#TODO: do I need to add more information about !B.
propose_prompt = r"""
You generate loop invariant candidates for ONE branch/phase of the loop body.

TASK:
Discover the correct loop invariant for the CURRENT branch.

GOAL:
Produce an inductive invariant for the CURRENT branch such that:
- it holds whenever control reaches this branch
- it is preserved by one loop iteration
- together with the assertion in the program it helps prove correctness

RULES:
- NEVER mention unknown()
- Use ONLY variables appearing in the program
- Allowed operators: <= < >= > == + - * / % && ( )
- Each returned string must be ONE conjunctive term using &&
- NEVER use '||' anywhere in any returned string
- If a disjunction is needed, split it into multiple conjunctive terms
  and return them as separate elements in the list
- The list elements will later be connected with '||' to form the final DNF invariant

IMPORTANT GUIDELINES:
- Do NOT simply copy preconditions
- If a variable is updated in the loop, avoid non-inductive bounds on it
- If a variable is unchanged by the loop, preserve stable facts about it
- Prefer relations between variables over isolated bounds
- Prefer relations involving variables that appear in the assertion
- If behavior differs by parity, modulo, threshold, or branch case, return multiple conjunctive terms

CONTEXT:

Program:
{program}

CURRENT branch/phase:
{current_branch}

OUTPUT:
Return EXACTLY one JSON-like list of conjunctive terms and nothing else.

Example:
[
  "x % 2 == z && y >= x",
  "x % 2 != z && y >= x + 1"
]
"""


value_prompt = r'''
You are scoring how strong a set of branch-sensitive loop invariants is.

Input:
- A program with pre/post-conditions.
- A set of generated branch invariants.

Each branch invariant is represented as:

branch (<branch_condition>):
[
  "conjunct1 && conjunct2 && ...",
  "conjunctA && conjunctB && ..."
]

Interpretation:
- Each string in the list is ONE conjunctive term.
- The list represents a DISJUNCTION (DNF) over entry cases.
- Therefore the invariant for the branch is:

    (term_1) || (term_2) || ...

Example format:

branch (x < z):
[
  "x < z && w >= 0",
  "x < z && x + w == z"
]

branch (x >= z):
[
  "x >= z && w <= 0"
]

Your goal:
Give a single score (1–10) for how well the whole set of candidates helps prove correctness.

====================================================
SCALE (1–10)
====================================================
10 — Fully correct, inductive, branch-consistent, implies post-condition.
8–9 — Strong, mostly inductive, minor gaps.
6–7 — Moderately useful, partly inductive, missing some key facts.
5 — Weak; too incomplete to prove the post-condition.
3–4 — Incorrect or non-inductive in several branches.
2 — Clearly wrong; contradicts loop or pre-state.
1 — Useless, inconsistent, or impossible as invariants.

====================================================
CRITERIA
====================================================
Score based on:
1. Pre-condition compatibility.
2. Inductiveness within each branch.
3. Respect for branch semantics.
4. Helpfulness for proving the post-condition.
5. Consistency across branches (strong vs weak ones).

====================================================
TARGET
====================================================

Program:
{program}

Generated branch invariants:
{branch_to_candidate}

====================================================
STRICT OUTPUT
====================================================
Output ONLY a single integer 1–10.
No explanation, no text, no comments.

Score:
'''

refine_prompt = r"""
You are a loop invariant generator.

TASK:
Refine the current loop invariant for the CURRENT branch.

CONTEXT:
Program:
{c_program}

Counterexample:
{counterexample}

CURRENT branch:
{branch}

Previous Candidates:
{previous_candidates}

Other Branch Candidates:
{other_branch_candidates}

These candidates are provided for reference only.
They are intended to give you a more complete view of the overall loop invariant across different branches.
Use them to understand global variable relationships and improve the CURRENT branch invariant if helpful.
Do NOT modify or regenerate the other branch candidates.
Focus only on refining the invariant for the CURRENT branch.

Failed Terms:
{failed_terms}

SPECIAL:
{special}

RULES:
- NEVER mention unknown()
- Use ONLY variables from the program
- Allowed operators: <= < >= > == + - * / % && ( )
- Each returned string must be ONE conjunctive term using &&
- NEVER use '||'
- If disjunction is needed, split into multiple terms (DNF)
- Generate facts ONLY for the CURRENT branch

GUIDELINES:
- KEEP correct parts, FIX only wrong or missing parts
- Ensure the invariant is inductive (preserved by the loop)
- Avoid non-inductive bounds on updated variables
- Prefer relations between variables over simple bounds
- Use the counterexample only to identify what is wrong
- You may REFER to other branch candidates for consistent relationships
- You may LEARN from failed invariants to avoid repeating incorrect patterns

OUTPUT:
Return EXACTLY one JSON list of conjunctive terms.

Example:
[
  "x % 2 == z && y >= x",
  "x % 2 != z && y >= x + 1"
]
"""

select_prompt = r"""
You are a loop invariant ranking assistant.

TASK:
Given a C program, several loop invariant candidates, and for each candidate a counterexample,
select the MOST PROMISING candidate to refine next.

You must choose the candidate that is most likely to be turned into a correct invariant
with the smallest and most meaningful refinement.

IMPORTANT:
Do NOT rank candidates using only shallow rules such as:
- how many checks they passed
- how many clauses they contain
- whether they look simpler
- whether they satisfy more properties numerically

Instead, analyze:
1. why the counterexample occurs
2. whether the failure is fundamental or only local
3. whether the candidate already captures an important preserved relationship
4. whether the missing fix is small, natural, and structurally meaningful
5. whether the candidate is closer to a true inductive invariant than the others

COUNTEREXAMPLE FORMAT:
Each candidate has one counterexample of the form:

(pre_cex, loop_cex, post_cex)

where:
- pre_cex is either None or a state showing the invariant is wrong on entry
- loop_cex is either None or a pair (state_before, state_after) showing the invariant is not inductive
- post_cex is either None or a state showing the invariant is too weak to prove the assertion

GUIDELINES:
- A candidate that already captures the right variable relationship but fails on a small boundary case
  is often more promising than a weak candidate that passes more checks.
- Prefer candidates whose failure suggests a natural refinement.
- Avoid candidates built mainly from copied preconditions or obviously non-inductive bounds on updated variables.
- Prefer candidates that express preserved algebraic relations between important variables.
- If a candidate fails because one clause is slightly too weak or too strong, it may still be very promising.
- If a candidate misses the core relationship entirely, it is less promising even if its counterexample looks smaller.

INPUT:

Program:
{program}

Candidates and counterexamples:
{candidates_with_counterexamples}

OUTPUT:
Output EXACTLY the selected candidate (the full invariant string).
Do NOT generate a new invariant.
Do NOT modify it.
Do NOT output explanations or any extra text.
"""

judge_prompt = r"""
You are a program analysis assistant.

Your task is to determine whether a given program state is reachable in the C program.

======================
INPUT
======================

C Program:
{c_program}

Counterexample:
{counterexample}

The counterexample is a tuple of two states:
- The first state is the program state BEFORE a loop iteration.
- The second state is the program state AFTER one loop iteration.

Your task is to judge ONLY the FIRST state.

======================
TASK
======================

Determine whether the FIRST state (the state before the loop iteration)
is reachable during real execution of the program.

When reasoning about reachability, consider:

- program initialization
- assume(...) constraints
- assignments before the loop
- loop structure
- variable updates inside the loop

Ignore:
- unknown() conditions
- solver artifacts
- temporary variables not affecting reachability

======================
OUTPUT RULE
======================

Return ONLY one word:

YES   -> if the first state can occur in some execution of the program
NO    -> if the first state is impossible to reach in the program

Do NOT output explanations.
Do NOT output additional text.
Only output YES or NO.
"""


direct_inv_prompt = r"""
You are a loop invariant generator.

======================
TASK
======================
Given a C program with a loop, generate a loop invariant that is:

1. TRUE before the loop starts (pre-condition)
2. PRESERVED by every loop iteration (inductive)
3. STRONG enough to prove the post-condition

======================
OUTPUT REQUIREMENT
======================
Return the invariant in **Disjunctive Normal Form (DNF)**:

- A disjunction (OR) of one or more conjunctive terms
- Each term is a conjunction of atomic constraints using &&

Form:
(inv_1) || (inv_2) || ... || (inv_n)

======================
STRICT RULES
======================
- NEVER mention unknown()
- Use ONLY variables from the program
- Allowed operators: <= < >= > == + - * / % && ||
- Do NOT use: max, min, ite, ?:, =>, <=>, true, false, function calls
- Each disjunct must be enclosed in parentheses
- Keep expressions simple and inductive

======================
GUIDELINES
======================
1. First understand how variables evolve in the loop:
   - Which variables increase/decrease?
   - Which variables remain unchanged?
   - Are there phase changes or conditional behaviors?

2. Identify preserved relationships:
   - Linear relations (e.g., y >= x)
   - Equalities or affine relations
   - Modulo/parity relations if relevant

3. If the loop has multiple behaviors (e.g., branches),
   use multiple disjuncts (DNF) to capture different cases.

4. Prefer relations involving variables appearing in the post-condition.

======================
PROGRAM
======================
{program}

======================
OUTPUT
======================
Output ONLY the invariant in DNF form, with no explanation.
"""

direct_refine_prompt = r"""
You are a loop invariant generator.

======================
TASK
======================
Given:
1. a C program,
2. a current loop invariant candidate,
3. a counterexample showing why the invariant failed,

generate a refined loop invariant.

The refined invariant must be:

1. TRUE before the loop starts
2. PRESERVED by every loop iteration
3. STRONG enough to prove the post-condition

======================
CURRENT INVARIANT
======================
{current_invariant}

======================
COUNTEREXAMPLE FORMAT
======================
The counterexample has the form:

[pre_cex, loop_cex, post_cex]

where:

- pre_cex is either None or a single state violating the pre-condition check
- loop_cex is either None or a pair of states:
    (state_before_iteration, state_after_iteration)
  showing the invariant is not inductive
- post_cex is either None or a single state violating the post-condition check

Example:
[None, ({{'y': '17', 'tmp': '0', 'x': '17'}}, {{'x': '34', 'y': '1', 'tmp': '0'}}), {{'y': '17', 'x': '17'}}]

Interpretation:
- pre_cex = None means no pre-condition violation found
- loop_cex != None means the invariant failed to be preserved by one loop step
- post_cex != None means the invariant is too weak to prove the post-condition

======================
HOW TO USE THE COUNTEREXAMPLE
======================

1. If pre_cex is not None:
   - the invariant is too strong or incorrect on an initial state
   - revise it so that it holds on valid pre-states

2. If loop_cex is not None:
   - the invariant is not inductive
   - use the transition (before -> after) to infer which relationship is not preserved
   - refine the invariant so it is preserved by the loop update

3. If post_cex is not None:
   - the invariant is too weak to prove the post-condition
   - strengthen it using relations relevant to the assertion

4. If multiple counterexamples are not None:
   - refine the invariant so that it addresses all of them together

======================
STRICT RULES
======================
- NEVER mention unknown()
- Use ONLY variables from the program
- Allowed operators: <= < >= > == + - * / % && ||
- Do NOT use: max, min, ite, ?:, =>, <=>, true, false, function calls
- Output the invariant in DNF form:
    (inv_1) || (inv_2) || ... || (inv_n)
- Each disjunct must be a conjunction of atomic constraints joined by &&
- Each disjunct must be enclosed in parentheses
- Do NOT output explanations

======================
GUIDELINES
======================
1. First reason about how the loop executes:
   - which variables are updated
   - which variables are unchanged
   - what relations are preserved

2. Do NOT simply patch the exact counterexample values.
   Infer the general relation that should hold.

3. Avoid non-inductive copied preconditions on updated variables.

4. Prefer algebraic relations between variables, especially variables used in the post-condition.

5. If the loop has multiple behaviors, use multiple disjuncts in DNF.

======================
PROGRAM
======================
{program}

======================
COUNTEREXAMPLE
======================
{counterexample}

======================
OUTPUT
======================
Output ONLY the refined loop invariant in DNF form, with no explanation.
"""


