import argparse
import os, sys, time

# Make the modules under src/ importable when running `python main.py` from
# the repo root, without requiring `pip install -e .` or setting PYTHONPATH.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from core import get_task
from search.bfs import refine_solve,naive_solve, CoT_solve
from core.loop import LoopInvSolver
from models import gpt_usage

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--backend', type=str,
                        choices=['gpt-4', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-5.1', 'gpt-5-nano', 'gpt-5.2', 'GPT-5.4'],
                        default='gpt-5.1')
    parser.add_argument('--temperature', type=float, default=0.9)
    parser.add_argument('--task', type=str, default='loop',
                        choices=['loop'])
    parser.add_argument('--task_idx', type=int, default=1, help='Index of the task to solve')

    parser.add_argument('--naive_run', action='store_true')
    parser.add_argument('--prompt_sample', type=str, choices=['standard', 'cot'])

    parser.add_argument('--method_generate', type=str, choices=['sample', 'propose'], default='propose')
    parser.add_argument('--method_evaluate', type=str, choices=['value', 'vote'], default='value')
    parser.add_argument('--method_select', type=str, choices=['sample', 'greedy'], default='greedy')

    parser.add_argument('--n_generate_sample', type=int, default=5)
    parser.add_argument('--n_evaluate_sample', type=int, default=3)
    parser.add_argument('--n_select_sample', type=int, default=5)

    parser.add_argument(
        '--category', choices=['Linear', 'NL', 'Multiphase'], default='Linear',
        help='Type of program/benchmark: Linear, NL (non-linear), or Multiphase'
    )
    parser.add_argument('--max_workers', type=int, default=8)
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--max_tokens', type=int, default=4096)
    parser.add_argument('--n_initial_refinements', type=int, default=5)
    parser.add_argument('--to_print', action='store_true', help='Whether to print detailed logs during solving')
    return parser.parse_args()

def wrap_usage(usage):
    return f"Prompt tokens: {usage.get('prompt_tokens')}\n" \
           f"Completion tokens: {usage.get('completion_tokens')}\n" \
           f"Estimated cost (USD): {usage.get('cost')}\n" \
           f"Number of queries: {usage.get('num_queries')}\n"

def main():
    args = parse_args()
    start_time = time.time()
    task = get_task(args.task)
    loop_invariant = refine_solve(args, task, args.task_idx, to_print=args.to_print)
    #loop_invariant = naive_solve(args, task, args.task_idx, to_print=args.to_print)
    #loop_invariant = CoT_solve(args, task, args.task_idx, to_print=args.to_print)
    end_time = time.time()
    usage = gpt_usage(backend=args.backend)
    print(f'found a solution for task {args.task_idx}: {loop_invariant}')
    print(f"Total time taken: {end_time - start_time} seconds")
    print("=== LLM Usage ===")
    print(wrap_usage(usage))





if __name__ == "__main__":
    main()