import json
import itertools


def strip_outer_parens(expr: str) -> str:
    expr = expr.strip()
    while expr.startswith("(") and expr.endswith(")"):
        depth = 0
        ok = True
        for i, ch in enumerate(expr):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth == 0 and i != len(expr) - 1:
                ok = False
                break
        if ok:
            expr = expr[1:-1].strip()
        else:
            break
    return expr


def split_top_level(expr: str, op: str) -> list[str]:
    expr = expr.strip()
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


def expand_expr_to_conj_terms(expr: str) -> list[str]:
    expr = strip_outer_parens(expr)
    if not expr:
        return []

    factors = split_top_level(expr, "&&")
    choices_per_factor = []

    for factor in factors:
        factor = strip_outer_parens(factor)
        if not factor:
            continue

        # split OR first, then remove unknown disjuncts only
        disjuncts = split_top_level(factor, "||")
        normalized = []

        for d in disjuncts:
            d = strip_outer_parens(d)
            if not d:
                continue
            if "unknown" in d:
                continue
            normalized.append(d)

        # if all disjuncts were removed, drop this factor entirely
        if normalized:
            choices_per_factor.append(normalized)

    if not choices_per_factor:
        return []

    results = []
    for combo in itertools.product(*choices_per_factor):
        term_parts = [strip_outer_parens(x) for x in combo if x.strip()]
        if term_parts:
            results.append(" && ".join(term_parts))

    return results


def clean_candidates(candidates: list[str]) -> list[list[str]]:
    cleaned = []

    for cand in candidates:
        try:
            parsed = json.loads(cand)
        except Exception:
            continue

        if not isinstance(parsed, list):
            continue

        inner = []
        for expr in parsed:
            if not isinstance(expr, str):
                continue
            expanded = expand_expr_to_conj_terms(expr)
            inner.extend(expanded)

        seen = set()
        deduped = []
        for item in inner:
            if item not in seen:
                seen.add(item)
                deduped.append(item)

        if deduped:
            cleaned.append(deduped)

    return cleaned
def run_tests():
    tests = [
        {
            "name": "simple single conjunction",
            "inp": ['[\n  "x >= y && y >= 100000"\n]'],
            "out": [["x >= y && y >= 100000"]],
        },
        {
            "name": "simple two candidates",
            "inp": ['[\n  "x >= y && y >= 100000"\n]', '[\n  "x >= y"\n]'],
            "out": [["x >= y && y >= 100000"], ["x >= y"]],
        },
        {
            "name": "one OR inside parentheses",
            "inp": ['["a > 0 && (z == 1 || z == 0) && b > 0"]'],
            "out": [["a > 0 && z == 1 && b > 0", "a > 0 && z == 0 && b > 0"]],
        },
        {
            "name": "two OR groups",
            "inp": ['["(x == 0 || x == 1) && (z == 0 || z == 1) && y > 0"]'],
            "out": [[
                "x == 0 && z == 0 && y > 0",
                "x == 0 && z == 1 && y > 0",
                "x == 1 && z == 0 && y > 0",
                "x == 1 && z == 1 && y > 0",
            ]],
        },
        {
            "name": "remove unknown factor",
            "inp": ['["a > 0 && unknown() && b > 0"]'],
            "out": [["a > 0 && b > 0"]],
        },
        {
            "name": "remove unknown disjunct",
            "inp": ['["a > 0 && (z == 1 || unknown()) && b > 0"]'],
            "out": [["a > 0 && z == 1 && b > 0"]],
        },
        {
            "name": "multiple expressions in one JSON list",
            "inp": ['["x >= y", "a > 0 && (z == 1 || z == 0) && b > 0"]'],
            "out": [[
                "x >= y",
                "a > 0 && z == 1 && b > 0",
                "a > 0 && z == 0 && b > 0",
            ]],
        },
        {
            "name": "nested outer parentheses",
            "inp": ['["((a > 0)) && ((z == 1 || z == 0)) && ((b > 0))"]'],
            "out": [["a > 0 && z == 1 && b > 0", "a > 0 && z == 0 && b > 0"]],
        },
        {
            "name": "invalid JSON ignored",
            "inp": ['not a json', '["x >= y"]'],
            "out": [["x >= y"]],
        },
    ]

    for t in tests:
        got = clean_candidates(t["inp"])
        assert got == t["out"], f"{t['name']} failed\nexpected={t['out']}\ngot={got}"
        print(f"PASS: {t['name']}")


if __name__ == "__main__":
    run_tests()