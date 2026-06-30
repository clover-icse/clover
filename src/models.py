import os
from openai import OpenAI, APIError
import backoff

completion_tokens = prompt_tokens = num_query = 0

client = OpenAI()

@backoff.on_exception(backoff.expo, APIError)
def completions_with_backoff(**kwargs):
    try:
        return client.chat.completions.create(**kwargs)
    except APIError as e:
        print("APIError occurred:")
        print(e)  # full readable error
        print(e.args)  # details
        raise  # MUST re-raise so backoff retries

def gpt(prompt, model="gpt-5-nano", temperature=0.7, max_tokens=1000, n=1, stop=None, debug=False) -> list:
    messages = [{"role": "user", "content": prompt}]
    output = chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    return output
    
def chatgpt(messages, model="gpt-5-nano", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens, num_query
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_completion_tokens=max_tokens, n=cnt, stop=stop)
        outputs.extend([choice.message.content for choice in res.choices])
        # log completion tokens
        completion_tokens += res.usage.completion_tokens
        prompt_tokens += res.usage.prompt_tokens
        num_query += 1
    return outputs
    
def gpt_usage(backend="gpt-5-nano"):
    global completion_tokens, prompt_tokens, num_query
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    elif backend == "gpt-4o":
        cost = completion_tokens / 1000 * 0.00250 + prompt_tokens / 1000 * 0.01
    elif backend == "gpt-5-nano":
        cost = prompt_tokens / 1_000_000 * 0.05 + completion_tokens / 1_000_000 * 0.40
    elif backend == "gpt-5.1" or backend == "gpt-5" or backend == "gpt-5.2":
        cost = prompt_tokens / 1_000_000 * 1.25 + completion_tokens / 1_000_000 * 10.00
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost, "num_queries": num_query}
