
from __future__ import annotations  # allow `str | None` style hints on Python 3.9

import itertools
import re


def strip_outer_parens(expr: str) -> str:
    """
    Repeatedly strip a single pair of outer parentheses if they wrap
    the whole expression.
    """
    expr = expr.strip()
    while expr.startswith("(") and expr.endswith(")"):
        depth = 0
        wraps_all = True
        for i, ch in enumerate(expr):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth == 0 and i != len(expr) - 1:
                wraps_all = False
                break
        if wraps_all:
            expr = expr[1:-1].strip()
        else:
            break
    return expr


def split_top_level(expr: str, op: str) -> list[str]:
    """
    Split by a top-level operator such as '&&' or '||',
    ignoring nested parentheses.
    """
    expr = expr.strip()
    if not expr:
        return []

    parts = []
    depth = 0
    start = 0
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1

        if depth == 0 and expr[i:i + len(op)] == op:
            parts.append(expr[start:i].strip())
            start = i + len(op)
            i += len(op)
            continue
        i += 1

    parts.append(expr[start:].strip())
    return [p for p in parts if p]


def is_dnf(expr: str) -> bool:
    """
    Check whether expr is in DNF:
        (conjunction) || (conjunction) || ...
    where each conjunct does not contain a top-level '||'.
    """
    expr = strip_outer_parens(expr)
    if not expr:
        return False

    disjuncts = split_top_level(expr, "||")
    for disj in disjuncts:
        disj = strip_outer_parens(disj)
        conjuncts = split_top_level(disj, "&&")
        for conj in conjuncts:
            conj = strip_outer_parens(conj)
            if len(split_top_level(conj, "||")) > 1:
                return False
    return True


def _expand_expr_to_dnf_terms(expr: str) -> list[str]:
    """
    Expand expressions like:
        a && (b || c) && d
    into:
        ['a && b && d', 'a && c && d']

    This is a syntactic converter intended for the invariant forms used here.
    """
    expr = strip_outer_parens(expr)
    if not expr:
        return []

    factors = split_top_level(expr, "&&")
    if not factors:
        return []

    choices_per_factor = []
    for factor in factors:
        factor = strip_outer_parens(factor)
        disjuncts = split_top_level(factor, "||")
        disjuncts = [strip_outer_parens(d) for d in disjuncts if d.strip()]
        if not disjuncts:
            return []
        choices_per_factor.append(disjuncts)

    results = []
    for combo in itertools.product(*choices_per_factor):
        pieces = [strip_outer_parens(x) for x in combo if x.strip()]
        if pieces:
            results.append(" && ".join(pieces))
    return results


def ensure_dnf(expr: str) -> str | None:
    """
    If expr is already DNF, return it.
    Otherwise try to convert it to DNF.
    If conversion fails, return None.
    """
    expr = strip_outer_parens(expr)
    if not expr:
        return None

    if is_dnf(expr):
        return expr

    try:
        terms = _expand_expr_to_dnf_terms(expr)
        if not terms:
            return None

        dnf_expr = " || ".join(f"({term})" for term in terms)
        return dnf_expr if is_dnf(dnf_expr) else None
    except Exception:
        return None


def _normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def run_tests() -> None:
    tests = [
        {
            "name": "already dnf simple",
            "expr": "(a && b) || (c && d)",
            "expected": "(a && b) || (c && d)",
        },
        {
            "name": "single conjunction is dnf",
            "expr": "x >= y && y >= 100000",
            "expected": "x >= y && y >= 100000",
        },
        {
            "name": "simple inner or",
            "expr": "a && (b || c) && d",
            "expected": "(a && b && d) || (a && c && d)",
        },
        {
            "name": "two or groups",
            "expr": "(x == 0 || x == 1) && (z == 0 || z == 1) && y > 0",
            "expected": (
                "(x == 0 && z == 0 && y > 0) || "
                "(x == 0 && z == 1 && y > 0) || "
                "(x == 1 && z == 0 && y > 0) || "
                "(x == 1 && z == 1 && y > 0)"
            ),
        },
        {
            "name": "user example",
            "expr": "(x >= 0 && x <= 999 && y >= 0 && z >= 0 && (z == 2 * (y - x) || z == 2 * (y - x) - 2000))",
            "expected": (
                "(x >= 0 && x <= 999 && y >= 0 && z >= 0 && z == 2 * (y - x)) || "
                "(x >= 0 && x <= 999 && y >= 0 && z >= 0 && z == 2 * (y - x) - 2000)"
            ),
        },
        {
            "name": "nested outer parentheses",
            "expr": "(((a && (b || c))))",
            "expected": "(a && b) || (a && c)",
        },
        {
            "name": "or at top level already dnf",
            "expr": "(p && q) || (r && s) || (t)",
            "expected": "(p && q) || (r && s) || (t)",
        },
    ]

    for t in tests:
        got = ensure_dnf(t["expr"])
        assert got is not None, f"{t['name']} failed: got None"
        assert _normalize_spaces(got) == _normalize_spaces(t["expected"]), (
            f"{t['name']} failed\n"
            f"expected: {t['expected']}\n"
            f"got     : {got}"
        )
        print(f"PASS: {t['name']}")

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
