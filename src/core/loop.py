import json
import os.path
from typing import List, Dict, Literal
from core.base import Task, LOOP_DATA_PATH
from core.c_inv_checker import inv_solver
from templates.loop import *
import re, ast
from dataclasses import dataclass
import json

def extract_safe_clauses(candidates: list[str], broken_terms: list[list[str]]):
    """
    Extract safe clauses for each candidate.

    candidates:
        ["x >= z && x % 2 == 0 && w >= 0", ...]

    broken_terms:
        [["w >= 0"], ...]

    return:
        [
            ["x >= z", "x % 2 == 0"],
            ...
        ]
    """

    all_safe = []

    for candidate, broken in zip(candidates, broken_terms):

        clauses = [c.strip() for c in candidate.split("&&")]
        broken_set = {b.strip() for b in broken}

        safe = [clause for clause in clauses if clause not in broken_set]

        all_safe.append(safe)

    return all_safe
@dataclass(frozen=True)
class CounterExample:
    position: int
    counterexample: str
    loop_candidate: str

def split_top_level_or(expr: str):
    parts = []
    buf = []
    depth = 0
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        if ch == '(':
            depth += 1
            buf.append(ch)
        elif ch == ')':
            depth -= 1
            buf.append(ch)

        elif ch == '|' and i + 1 < n and expr[i + 1] == '|' and depth == 0:
            # we hit a top-level ||
            part = "".join(buf).strip()
            if part:
                parts.append(part)
            buf = []
            i += 1  # skip second '|'
        else:
            buf.append(ch)

        i += 1

    # last part
    part = "".join(buf).strip()
    if part:
        parts.append(part)
    return parts


def broken_clauses_json_safe(raw_clauses, counterexample):
    """
    raw_clauses: either a list of strings or a JSON string representing a list
    counterexample: dict of variable assignments

    Returns: list of all conjunctive terms broken by the counterexample
    """
    broken = []

    # if string, try to load JSON
    if isinstance(raw_clauses, str):
        try:
            clauses_list = json.loads(raw_clauses)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON: {raw_clauses}")
    elif isinstance(raw_clauses, list):
        clauses_list = raw_clauses
    else:
        raise TypeError(f"raw_clauses must be list or JSON string, got {type(raw_clauses)}")

    # make sure counterexample values are numeric if needed
    valuation = {k: float(v) if isinstance(v, str) and v.lstrip('-').isdigit() else v
                 for k, v in counterexample.items()}

    # iterate over each clause
    for clause in clauses_list:
        # split conjunctive terms
        terms = [t.strip() for t in clause.split("&&")]
        for term in terms:
            if not term:
                continue
            try:
                if not eval(term, {}, valuation):
                   broken.append(term)
            except:
                # if evaluation fails, consider it broken
                broken.append(term)
    return broken
def verify_invariant_format(output_str: str) -> bool:
    """
    Verify that the output follows the required invariant format.

    Rules checked:
    - Output must be a Python-style list
    - Each element must be a string
    - Each string must be a conjunction using '&&' (single atom also OK)
    - No '||' allowed
    - No empty conjuncts
    - Only allowed characters (now includes '&' for '&&')
    """

    try:
        data = ast.literal_eval(output_str)
    except Exception:
        return False

    # Must be a list
    if not isinstance(data, list) or len(data) == 0:
        return False

    for term in data:
        # Each element must be a string
        if not isinstance(term, str):
            return False

        # Disallow disjunction
        if "||" in term:
            return False

        # Split conjunction
        atoms = [a.strip() for a in term.split("&&")]

        # No empty atoms (catches trailing/leading '&&' too)
        if any(len(a) == 0 for a in atoms):
            return False

        # Basic allowed character check (FIXED: includes '&')
        if not re.fullmatch(r"[a-zA-Z0-9_<>=+\-*/()& \t]+", term):
            return False

    return True

class LoopInvSolver(Task):
    def __init__(self):
        super().__init__()
        self.value_cache = {}
        self.counterexamples: List[CounterExample] = []
        self.inv2list_cache = {} # cache for invariant to list conversion
        self.candidates_to_raw_counterexamples : Dict[str, List[str]] = {} # map from candidate string to raw counterexample string
        self.wrapped_to_unwrapped_candidates = {}

    def clean_candidates(self, candidates: List[List[str]]) -> List[List[str]]:
        cleaned = []

        for cand in candidates:
            try:
                parsed = json.loads(cand)
            except:
                continue

            inner = []

            for expr in parsed:

                # discard whole expression if contains ||
                if "||" in expr:
                    continue

                parts = [p.strip() for p in expr.split("&&")]

                # remove clauses containing unknown()
                parts = [p for p in parts if "unknown" not in p]

                if not parts:
                    continue

                new_expr = " && ".join(parts)
                inner.append(new_expr)

            if inner:
                cleaned.append(inner)

        return cleaned

    def unwrap_output(self, ys):
        all_candidates = []

        for y in ys:
            clauses = []

            for clause in y:

                # If clause is already a list (LLM sometimes outputs parsed objects)
                if isinstance(clause, list):
                    parsed = clause

                # If clause is a JSON string
                elif isinstance(clause, str):
                    parsed = json.loads(clause)

                else:
                    continue

                for c in parsed:
                    clauses.append(f"({c})")

            candidate = " || ".join(clauses)

            # store mapping
            self.wrapped_to_unwrapped_candidates[candidate] = y

            all_candidates.append(candidate)

        return all_candidates

    def get_unwrapped_candidate(self, candidate):
        return self.wrapped_to_unwrapped_candidates.get(candidate)

    def test_output(self, loop_candidate: str , output: str):
        if output in self.candidates_to_raw_counterexamples:
            self.store_counterexample(output)
            return False
        try:
            result = inv_solver(self.vc_file,  output)
            if result != [None, (None,None), None]:
                self.candidates_to_raw_counterexamples[output] = result
                self.store_counterexample(output)
            return result == [None, (None,None), None]
        except Exception as e:
            print(f"Error during invariant checking: {e}")
            return False

    def get_counterexample_branch(self, candidate):
        result = self.candidates_to_raw_counterexamples.get(candidate)
        pre, loop, post = result
        # determine failing position
        if pre is not None:
            cex = pre
            position = 'pre'
        elif loop != (None, None):
            cex = loop
            position = 'loop'
        elif post is not None:
            cex = post
            position = 'post'
        else:
            return None
        def normalize_dict(d):
            return {
                k: int(v) if isinstance(v, str) and v.lstrip('-').isdigit() else v
                for k, v in dict(d).items()
            }

        if isinstance(cex, tuple) and len(cex) == 2:
            valuation = tuple(
                normalize_dict(e) if hasattr(e, "items") else e
                for e in cex
            )
        else:
            valuation = normalize_dict(cex) if hasattr(cex, "items") else cex

        # clean branch predicates (remove unknown())
        cleaned_branches = []
        for b in self.branches:

            # remove unknown() and !unknown()
            b = re.sub(r'!?unknown\(\)', '', b)

            # split by &&
            parts = [p.strip() for p in b.split("&&")]
            cleaned_parts = []
            for p in parts:
                p = p.strip()

                # remove outer parentheses safely
                while p.startswith("(") and p.endswith(")"):
                    p = p[1:-1].strip()

                if p:
                    cleaned_parts.append(p)

            if cleaned_parts:
                cleaned_branches.append(" && ".join(cleaned_parts))
            else:
                cleaned_branches.append("")

        def find_branch(val):
            for i, cond in enumerate(cleaned_branches):
                if cond == "":
                    continue
                try:
                    cond = cond.replace("&&", "and")
                    if eval(cond, {}, val):
                        return i
                except:
                    pass
            return None

        # determine branch index
        if isinstance(valuation, tuple):
            branch1 = find_branch(valuation[0])
            branch2 = find_branch(valuation[1])

            if branch1 == branch2:
                branch_index = branch1
            else:
                branch_index = (branch1, branch2)
        else:
            branch_index = find_branch(valuation)

        return (valuation, branch_index, position)
    def get_input(self, idx: int, category : Literal['Linear', 'NL', 'Multiphase']) -> str:
        self.vc_file = os.path.join(LOOP_DATA_PATH, category, 'c_smt2', f'{idx}.c.smt')
        self.c_file = os.path.join(LOOP_DATA_PATH, category, 'c', f'{idx}.c')
        branch_path = os.path.join(LOOP_DATA_PATH, category, 'c_branches', f'{idx}_branches.txt')

        with open(branch_path, "r", encoding="utf-8") as f:
            self.branches = json.load(f)

        # remove branches that only contain unknown() (no real condition)
        self.branches = [
            b for b in self.branches
            if not ("unknown()" in b and "&&" not in b)
        ]

        self.steps = len(self.branches)
        assert os.path.exists(self.vc_file) and os.path.exists(self.c_file) and os.path.exists(branch_path), f'Files for index {idx} do not exist.'
        with open(self.c_file, 'r') as f:
            code = f.read()

        return code

    def sort_candidates(self, candidates):

        def score(candidate):
            result = self.candidates_to_raw_counterexamples.get(candidate)

            if result is None:
                return (0, 0, 0, 0)

            pre, loop, post = result

            # count None values
            none_count = sum([
                pre is None,
                loop == (None, None),
                post is None
            ])

            # priority flags (1 = good)
            loop_ok = int(loop == (None, None))
            post_ok = int(post is None)
            pre_ok = int(pre is None)

            return (none_count, loop_ok, post_ok, pre_ok)

        return sorted(candidates, key=score, reverse=True)

    def propose_prompt_wrap(self, x: str,  i : int = None) -> str:
        return propose_prompt.format(
            program=x,
            current_branch=self.branches[i],
        )

    def judge_prompt_wrap(self, x: str, counterexample: str) -> str:
        return judge_prompt.format(
            c_program=x,
            counterexample=counterexample,
        )
    def get_current_invariant(self, y: List[str]) -> str:
        result = ''
        for i in range(len(y)):
            result += f'branch {self.branches[i]} : candidates {y[i]}\n'
        return  result

    def value_prompt_wrap(self, x: str, y : List[str]) -> str:

        return value_prompt.format(
            program=x,
            branch_to_candidate=self.get_current_invariant(y),
        )

    def wrap_select_prompt(self, x: str,candidates: str) -> str:
        def candidates_with_counterexamples():
            result = ''
            for c in candidates:
                if c in self.candidates_to_raw_counterexamples:
                    result += f"Candidate: {c}\nCounterexample: {self.candidates_to_raw_counterexamples[c]}\n\n"
                else:
                    result += f"Candidate: {c}\nCounterexample: SYNTAX ERROR\n\n"
            return result
        return select_prompt.format(
            program=x,
            candidates_with_counterexamples=candidates_with_counterexamples(),
        )
    def refine_prompt_wrap(self,x, counterexample: str, branch_index : int,position : str, unwraped_candidates: str, failed_clauses, special) -> str:
        if special == "first":
            special = """
        Counterexample interpretation:

        The counterexample is a tuple (pre_state, post_state).

        The pre_state is NOT reachable in the real program, so this counterexample is spurious.

        Refinement goal:
        - Strengthen the invariant to exclude such unreachable states
        - Ensure the invariant still holds for all reachable executions in this branch

        Guidelines:
        - Do NOT overfit to the exact values in the counterexample
        - Derive general constraints from program logic
        - Keep the invariant consistent with the branch condition
        - Ignore any unknown() terms
        """
        elif special == "second":
            special = """
        Counterexample interpretation:

        The counterexample is a tuple (pre_state, post_state) representing a loop transition.

        The pre_state is reachable, but the invariant is NOT preserved after the loop iteration.

        Refinement goal:
        - Make the invariant inductive (preserved across the transition)

        Guidelines:
        - Identify which clause becomes false in post_state
        - Modify or replace that clause so it remains true after the update
        - Keep clauses that are already correct
        - Ensure the invariant remains valid for the CURRENT branch
        - Ignore any unknown() terms when reasoning about the branch condition
        """
        elif position == "pre":
            special = """
        Counterexample interpretation:

        The counterexample is a reachable pre-state that does NOT satisfy the invariant.

        Refinement goal:
        - Adjust the invariant so it holds on all valid pre-states

        Guidelines:
        - Do NOT exclude valid initial states
        - Avoid overfitting to this specific counterexample
        - Make minimal changes while preserving useful structure
        """
        elif position == "post":
            special = """
        Counterexample interpretation:

        The counterexample is a state where the invariant holds, but the post-condition is violated.

        Refinement goal:
        - Strengthen the invariant so it is sufficient to prove the post-condition

        Guidelines:
        - Add missing constraints needed for correctness
        - Prefer relations involving variables in the assertion
        - Avoid overfitting to the specific counterexample
        """
        else:
            special = ""
        return refine_prompt.format(
            c_program=x,
            counterexample=counterexample,
            branch=self.branches[branch_index],
            position=position,
            previous_candidates= unwraped_candidates[branch_index],
            other_branch_candidates="\n".join(
                f"{self.branches[i]} : {c}"
                for i, c in enumerate(unwraped_candidates)
                if i != branch_index
            ),
            failed_terms=failed_clauses,
            special=special,
        )

    def value_outputs_unwrap(self, x: str, y: str, value_outputs: list) -> float:
        # convert strings like "4" into integers
        scores = [float(v) for v in value_outputs]

        # compute the mean score
        return sum(scores) / len(scores)

    def store_counterexample(self, output: str):
        """Store a single CounterExample object (no dedup logic)."""
        self.counterexamples.append(output)

    def reset_counterexamples(self):
        self.counterexamples = []
    def wrap_direct_inv_prompt(self, x: str) -> str:
        return direct_inv_prompt.format(program=x)
    def wrap_direct_refine_prompt(self, x: str, candidate: str) -> str:
        return direct_refine_prompt.format(
            program=x,
            counterexample=self.candidates_to_raw_counterexamples.get(candidate, "None"),
            current_invariant=candidate,
        )

