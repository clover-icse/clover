import itertools
from collections import Counter

import numpy as np
import time
from functools import partial
from models import gpt
from core.loop import *
from core.dnf_normalizer import clean_candidates
from core.dnf_utils_with_tests import ensure_dnf

def get_value(task, x, y, n_evaluate_sample, cache_value=True, final=False):
    value_prompt = task.value_prompt_wrap(x, y) if not final else task.final_value_prompt_wrap(x, y)
    str_y = task.get_current_invariant(y) if isinstance(y, list) else y
    if cache_value and str_y in task.value_cache:
        return task.value_cache[str_y]
    value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    if cache_value:
        task.value_cache[str_y] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True, final=False):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        str_y = task.get_current_invariant(y) if isinstance(y, list) else y
        if str_y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value, final=final)
            local_value_cache[str_y] = value
        values.append(value)
    return values



def get_proposals(task, x, i, n_generate_sample=1):
    propose_prompt = task.propose_prompt_wrap(x, i)
    #proposals = gpt(propose_prompt, n=5, stop=None)[0].split('\n')
    proposals = list(set(gpt(propose_prompt, n= 5, stop=None)))
    #proposals = [p for p in (p.strip() for p in proposals) if verify_invariant_format(p)]
    #proposals = clean_candidates(proposals)
    while proposals is None or len(proposals) == 0:
        print("LLM returned None for proposals, retrying...")
        time.sleep(1)
        proposals = gpt(propose_prompt, n= n_generate_sample, stop=None)
        proposals = [p for p in (p.strip() for p in proposals) if verify_invariant_format(p)]
    #return [y + _ + '\n' for _ in proposals]
    return proposals

# def get_refinements(task, x, y = None, i = None):
#     refine_prompt = task.refinement_prompt_wrap(x, y, i)
#     refinements = gpt(refine_prompt, n=1, stop=None)
#     return refinements
def get_samples(task, x, y, n_generate_sample, prompt_sample, stop):
    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x, y)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    samples = gpt(prompt, n=n_generate_sample, stop=stop)
    return [y + _ for _ in samples]

def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature, debug=to_print, max_tokens=args.max_tokens)
    print(gpt)
    x = task.get_input(idx, args.category)  # input
    ys = [[]]  # current output candidates
    infos = []
    for step in range(task.steps):

        new_ys = get_proposals(task, x,  step,args.n_generate_sample)

        # for y1 in ys:
        #     for y2 in new_ys:
        #
        # new_ys = list(itertools.chain(*new_ys))
        if to_print:
            print(f'proposals for step {step}: {new_ys}')

        combined_ys = []
        for y1 in ys:
            for y2 in new_ys:
                combined_ys.append(y1 + [y2])
        new_ys = combined_ys
        # new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))
        # evaluation
        values = get_values(task, x, new_ys, args.n_evaluate_sample)

        select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        select_new_ys = [new_ys[select_id] for select_id in select_ids]

        # log
        if to_print:
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')

        
        infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys
    
    if to_print: 
        print(ys)
    return ys, x

def CoT_solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature, debug=to_print, max_tokens=args.max_tokens)
    print(gpt)
    x = task.get_input(idx, args.category)  # input
    ys = [[]]  # current output candidates
    for step in range(task.steps):

        new_ys = get_proposals(task, x, step, 1)
        # for y1 in ys:
        #     for y2 in new_ys:
        #
        # new_ys = list(itertools.chain(*new_ys))
        combined_ys = []
        for y1 in ys:
            for y2 in new_ys:
                combined_ys.append(y1 + [y2])
        ys = combined_ys


    candidates = task.unwrap_output(ys)
    for c in candidates:
        if task.test_output(c, c):
            best = c
            return best
    if to_print:
        print("Refinement needed.")
    success = False
    while not success:
        #candidate = select_best_candidates(task,x, candidates)
        candidate = candidates[0]
        unwraped_candidates = task.get_unwrapped_candidate(candidate)
        valuation, branch_index, position = task.get_counterexample_branch(candidate)
        candidate, valuation = unwraped_candidates[branch_index[1] if isinstance(branch_index, tuple) else branch_index], valuation[1] if isinstance(valuation, tuple) else valuation
        broken_terms = broken_clauses_json_safe(candidate, valuation)
        special = None

        if to_print:
            print(f"Counterexample found: valuation={valuation}, broken_terms={broken_terms}", f"refining candidate: {candidates[0]}")
        ys = []
        if position == 'loop' and isinstance(branch_index, tuple):
            judge_answer = get_judge_answer(task, x, valuation)
            if judge_answer == 'NO':
                branch_index = branch_index[0]
                special = 'first'
                broken_terms = None
            else:
                branch_index = branch_index[1]
                special = 'second'
        refinements = get_refinements(
            task, x, valuation, branch_index, position,
            unwraped_candidates, broken_terms, special
        )

        for r in refinements:
            new_unwrapped = unwraped_candidates.copy()
            new_unwrapped[branch_index] = r
            ys.append(new_unwrapped)
        candidates = list(set(task.unwrap_output(ys)))
        # direct_refine_prompt = task.wrap_direct_refine_prompt(x, candidates[0])
        # candidates = gpt(direct_refine_prompt, n=5, stop=None)

        print("Refinements: ", candidates)
        for c in candidates:
            if task.test_output(c, c):
                best = c
                return best

def refine_solve(args, task, idx, to_print=True):
    ys, x= solve(args, task, idx, to_print=to_print)
    candidates = task.unwrap_output(ys)
    if to_print:
        print('candidates: ', candidates)
    best = None
    success = False
    for c in candidates:
        if task.test_output(c, c):
            best = c
            return best
    if to_print:
        print("Refinement needed.")
    while not success:
        candidate = select_best_candidates(task,x, candidates)
        unwraped_candidates = task.get_unwrapped_candidate(candidate)
        valuation, branch_index, position = task.get_counterexample_branch(candidate)
        candidate, valuation = unwraped_candidates[branch_index[1] if isinstance(branch_index, tuple) else branch_index], valuation[1] if isinstance(valuation, tuple) else valuation
        broken_terms = broken_clauses_json_safe(candidate, valuation)
        special = None

        if to_print:
            print(f"Counterexample found: valuation={valuation}, broken_terms={broken_terms}", f"refining candidate: {candidates[0]}", f"position: {position}, branch_index: {branch_index}")
        ys = []
        if position == 'loop' and isinstance(branch_index, tuple):
            judge_answer = get_judge_answer(task, x, valuation)
            if judge_answer == 'NO':
                branch_index = branch_index[0]
                special = 'first'
                broken_terms = None
            else:
                branch_index = branch_index[1]
                special = 'second'
        refinements = get_refinements(
            task, x, valuation, branch_index, position,
            unwraped_candidates, broken_terms, special
        )

        for r in refinements:
            new_unwrapped = unwraped_candidates.copy()
            new_unwrapped[branch_index] = r
            ys.append(new_unwrapped)
        candidates = list(set(task.unwrap_output(ys)))
        # direct_refine_prompt = task.wrap_direct_refine_prompt(x, candidates[0])
        # candidates = gpt(direct_refine_prompt, n=5, stop=None)

        print("Refinements: ", candidates)
        for c in candidates:
            if task.test_output(c, c):
                best = c
                return best

def select_best_candidates(task,x, candidates):
    prompt = task.wrap_select_prompt(x,candidates)
    responses = gpt(prompt, n=5, stop=None)
    # clean responses
    outputs = [r.strip() for r in responses if r]

    # count votes
    counts = Counter(outputs)

    # pick the most common valid one
    for cand, _ in counts.most_common():
        if cand in task.candidates_to_raw_counterexamples:
            return cand

    # fallback: return first valid candidate
    for cand in candidates:
        if cand in task.candidates_to_raw_counterexamples:
            return cand

    return candidates[0] if candidates else None

def get_refinements(task, x,  counterexample: str, branch_index : int, position : str, unwraped_candidates: str, failed_clauses, special : str)->list :
    refine_prompt = task.refine_prompt_wrap(x, counterexample, branch_index, position, unwraped_candidates, failed_clauses, special)
    refinements = list(set(gpt(refine_prompt, n=5, stop=None)))
    #refinements = [p for p in (p.strip() for p in refinements) if verify_invariant_format(p)]
    #refinements = clean_candidates(refinements)
    while refinements is None or len(refinements) == 0:
        print("LLM returned None for refinements, retrying...")
        time.sleep(1)
        refinements = gpt(refine_prompt, n=5, stop=None)
        refinements = [p for p in (p.strip() for p in refinements) if verify_invariant_format(p)]

    return refinements

def get_judge_answer(task, x, counterexample):
    judge_prompt = task.judge_prompt_wrap(x, counterexample)
    judge_answer = gpt(judge_prompt, n=1, stop=None)[0].strip().lower()
    judge_answer = judge_answer.strip().upper()
    while judge_answer not in ['YES', 'NO']:
        print(f"LLM returned unexpected judge answer: {judge_answer}, retrying...")
        time.sleep(1)
        judge_answer = gpt(judge_prompt, n=1, stop=None)[0].strip().lower()
    return judge_answer

def naive_solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx, args.category)  # input
    dir_pro =task.wrap_direct_inv_prompt(x)
    loop_candiate = gpt(dir_pro, n=1, stop=None)[0].strip()
    loop_candiate = ensure_dnf(loop_candiate)
    while not loop_candiate:
        loop_candiate = ensure_dnf(gpt(dir_pro, n=1, stop=None)[0].strip())
    print('initial candidate: ', loop_candiate)
    while not task.test_output(loop_candiate, loop_candiate):
        print('refining candidate: ', loop_candiate)
        direct_refine_prompt = task.wrap_direct_refine_prompt(x, loop_candiate)
        loop_candiate = ensure_dnf(gpt(direct_refine_prompt, n=1, stop=None)[0].strip())
        while not loop_candiate:
            loop_candiate = ensure_dnf(gpt(direct_refine_prompt, n=1, stop=None)[0].strip())
    return loop_candiate