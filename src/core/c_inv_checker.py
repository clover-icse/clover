import z3
import tokenize
import io
import logging
from z3 import *
import re
import random

p = {}
p["%"] = 4
p["*"] = 4
p["/"] = 4
p["+"] = 3
p["-"] = 3
p[">="] = 2
p[">"] = 2
p["=="] = 2
p["<="] = 2
p["<"] = 2
p["!="] = 2
p["and"] = 1
p['or'] = 1
p["("] = 0
p[")"] = 0

def infix_postfix(infix_token_list):
    # print(infix_token_list)
    # exit(0)
    opStack = []
    postfix = []

    for t in infix_token_list:
        if t not in p and t != "(" and t != ")":
            postfix.append(t)
        elif t == "(":
            opStack.append(t)
        elif t == ")":
            while len(opStack) > 0 and opStack[-1] != "(":
                postfix.append(opStack.pop())
            if len(opStack) > 0 and opStack[-1] == "(":
                opStack.pop()
            else:
                raise ValueError(") matching false")
        elif t in p:
            while len(opStack) > 0 and p[opStack[-1]] >= p[t]:
                postfix.append(opStack.pop())
            opStack.append(t)
        else:
            raise ValueError(f"Undefined: {t}")

    while len(opStack) > 0:
        top = opStack.pop()
        if top == "(":
            raise ValueError("( matching false")
        postfix.append(top)

    # print(postfix)
    # exit(0)

    return postfix

def postfix_prefix(postfix_token_list):
    # print(postfix_token_list)
    # exit(0)
    stack = []
    for t in postfix_token_list:
        if t not in p:
            stack.append(t)
        else:
            sub_stack = []
            sub_stack.append("(")
            sub_stack.append(t)
            op1 = stack.pop(-1)
            op2 = stack.pop(-1)
            sub_stack.append(op2)
            sub_stack.append(op1)
            
            sub_stack.append(")")
            stack.append(sub_stack)
    return stack

def stringify_prefix_stack(prefix_stack):
    s = ""
    for e in prefix_stack:
        if type(e) == list:
            s += stringify_prefix_stack(e)
        else:
            s += e + " "
    return s.strip()

def inv_checker(vc_file: str, inv: str, assignments):
    inv = inv.replace("&&", "and").replace("||", "or")
    b = io.StringIO(inv)
    inv_tokenized = [token for token in tokenize.generate_tokens(b.readline) if token.string != ""]
    
    # var_list = {token for token in inv_tokenized if token.isalpha() and token not in ("and", "or")}
    var_list = {token.string for token in inv_tokenized if token.type == tokenize.NAME and token.string not in ("and", "or")}
    
    var_dict = {var: 1 for var in var_list}
    for v, val in assignments:
        if v in var_dict:
            var_dict[v] = int(val)
    try:
        res = eval(inv, {}, var_dict) # using an empty global context and var_dict as local context
        return res
    except:
        return False

def parse_expression(expr):
    stack = []
    i = 0
    while i < len(expr):
        if expr[i] == '(':
            sub_expr, length = parse_expression(expr[i+1:])
            stack.append(f"( {sub_expr} )")
            i += length + 1
        elif expr[i] == ')':
            return process_stack(stack), i + 1
        else:
            stack.append(expr[i])
            i += 1
    return process_stack(stack), i

def process_stack(stack):
    expr = ''.join(stack).strip()

    # if expr.startswith('!='):
    #     left_paren_idx = expr.find('(')
    #     right_expr = expr[left_paren_idx:]
    #     return f"not ( = {right_expr.strip()} )"

    if expr.startswith('!='):
        return f"not ( = {expr[2:].strip()} )"
        # print("expr", expr)
        # if expr.count('(') > 0:
        #     left_paren_idx = expr.find('(')
        #     right_expr = expr[left_paren_idx:]
        #     return f"not ( = {right_expr.strip()} )"
        # else:
        #     parts = expr.split()
        #     # print("parts", parts)
        #     return f"not ( = {parts[1]} {parts[2]} )"

    return expr

def find_variables(m: z3.ModelRef, i: int):
    """
    Extract only program variables from a Z3 model.

    Parameters:
        m : z3.ModelRef
            The model returned by sol.model().
        i : int
            0 = pre-condition check
            1 = transition (inductiveness) check
            2 = post-condition / safety check

    Returns:
        If i == 0 or i == 2:
            dict: {var_name: value}
        If i == 1:
            tuple: ({pre_state_vars}, {post_state_vars})
    """

    # Matches helper temporaries like x_0, y_2, tmp_15, etc.
    temp_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*_\d+\b')

    # Meta function names we definitely want to drop from the model:
    meta_keys = {"inv-f", "pre-f", "post-f", "trans-f"}

    # -----------------------------
    # Helper: filter a single dict
    # -----------------------------
    def _filter_dict_from_model(model: z3.ModelRef, pick_post: bool = None):
        """
        Convert model to {name: value} and filter out:
        - temporaries like x_0, y_1, ...
        - meta entries like inv-f, pre-f, post-f, trans-f
        - if pick_post is not None and name ends with '!', route to post/pre
        """
        d = {}
        for sym in model:
            name = str(sym)
            val = str(model[sym])

            # Drop meta function symbols
            if name in meta_keys:
                continue

            # Drop helper temporaries like x_0, y_3, etc.
            if temp_pattern.fullmatch(name):
                continue

            # Generic keep (used for i == 0 or 2)
            d[name] = val

        return d

    # ---------------------------------------------
    # Case 1: pre-condition or post-condition check
    # ---------------------------------------------
    if i == 0 or i == 2:
        # Just return filtered variables
        return _filter_dict_from_model(m)

    # --------------------------------------
    # Case 2: transition (inductiveness) check
    # --------------------------------------
    else:
        pre_state = {}
        post_state = {}

        for sym in m:
            name = str(sym)
            val = str(m[sym])

            # Drop meta function symbols
            if name in meta_keys:
                continue

            # Drop helper temporaries like x_0, y_2, etc.
            if temp_pattern.fullmatch(name):
                continue

            # Next-state variables are usually written as x!, y!, ...
            if name.endswith("!"):
                post_state[name[:-1]] = val
            else:
                pre_state[name] = val

        return pre_state, post_state

def inv_solver(vc_file: str, inv: str):
    #print("inv", inv)
    inv = inv.replace("&&", "and", -1)
    inv = inv.replace("||", "or", -1)
    b = io.StringIO(inv)
    t = tokenize.generate_tokens(b.readline)
    tokens = list(t)
    inv_tokenized = []
    previous_token = None
    for index, token in enumerate(tokens):
        if token.string.strip() == "":
            previous_token = None
        if token.string.strip() != "":
            if token.string == "-" and tokens[index + 1].start[1] == token.end[1] and (tokens[index - 1].type != tokenize.NAME or tokens[index - 1].string == "or" or tokens[index - 1].string == "and") :
                previous_token = token
            elif previous_token is not None:
                if token.type == tokenize.NUMBER:
                    inv_tokenized.append(previous_token.string + token.string)
                elif token.type == tokenize.NAME:
                    inv_tokenized.append("(" + previous_token.string + " " + token.string + ")")
                previous_token = None
            else:
                inv_tokenized.append(token.string)
    inv = stringify_prefix_stack(postfix_prefix(infix_postfix(inv_tokenized)))
    inv = inv.replace("==", "=", -1)
    inv = inv.replace("%", "mod", -1)
    inv, _ = parse_expression(inv)

    #print("inv", inv)
    # exit(0)

    sol = z3.Solver()
    sol.set(auto_config=False)
    res = []

    vc_sections = [""]
    with open(vc_file, 'r') as vc:
        for vc_line in vc.readlines():
            if "SPLIT_HERE_asdfghjklzxcvbnmqwertyuiop" in vc_line:
                vc_sections.append("")
            else:
                vc_sections[-1] += vc_line
    assert len(vc_sections) == 5

    tpl = [vc_sections[0]]


    for i in range(2, 5):
        tpl.append(vc_sections[1] + vc_sections[i])
    res = []
    for i in range(3):
        s = tpl[0] + inv + tpl[i+1]
        # print("s", s)
        sol.reset()
        sol.set("timeout", 600000)
        try:
            decl = z3.parse_smt2_string(s)
        except Exception as e:
            # print(s)
            res.append("EXCEPT")
            continue
        # print("decl", decl)
        sol.add(decl)
        r = sol.check()
        if z3.sat == r:
            m = sol.model()
            ce = find_variables(m, i)
            res.append(ce)
        elif z3.unknown == r:
            if i == 0:
                w = "pre"
            elif i == 1:
                w = "loop"
            elif i == 2:
                w = "post"
            logging.warning("inv- " + inv + " solution unknown in " + w)
            res.append("EXCEPT")
            #print("inv", inv)
            raise Exception("SOL UNKNOWN")
        else:
            res.append(None) if i != 1 else res.append((None, None))
    # exit(0)
    return res

if __name__ == "__main__":
    vc_file = "../benchmarks/Multiphase/c_smt2/3.c.smt"
    #inv = "(x == 0 && w == 0 && y > z) || (x < z && w < z && y > z && z >= 0 && x - w == 0 && x >= 0) || (x >= 0 && x >= z && (2 * x + w == 3 * z || 2 * x + w == 0 ) && y > z) "
    # inv = 'x == 0 && (w == 0) && y > z || (w == x && x < z && z > 0 && y > z && x >= 0) || (w == -2 * (x - z) + z && x >= z && z > 0 && y > z) || (w == -2 * (x - 0)  && x >= z && z <= 0 && y > z) && x >= 0'
    inv ="""
(
 (x == 0 && w == 0) || (x > 0)
)"""
     # inv =  "((x < z) && (z > 0) && (x >= 0) && x == w)  || " \
     #  "((x >= z) && (z > 0) && (w == (-2) * (x - z) + z)) || " \
     #  "((x >= z) && (z <= 0) && (w == -2 * (x - 0))) && (y > z) && (x >= 0)"

    result = inv_solver(vc_file, inv)
    print("result", result)