import json
from typing import List
import asyncio
from .client import aclient, DEFAULT_MODEL, load_prompt

_prompt_titles_batch = load_prompt("generate_titles_batch")
_prompt_title_single = load_prompt("generate_title_single")
_prompt_check_title = load_prompt("check_title")


async def generate_titles(titles: List) -> tuple:
    messages = [
        {"role": "system", "content": _prompt_titles_batch},
        {"role": "user", "content": titles},
    ]
    response = await aclient.chat.completions.create(model=DEFAULT_MODEL, messages=messages)
    token_counts = (response.usage.prompt_tokens, response.usage.completion_tokens)
    print("Number of input tokens: ", response.usage.prompt_tokens)
    print("Number of output tokens: ", response.usage.completion_tokens)
    output = response.choices[0].message.content
    return json.loads(output), token_counts


async def generate_title(text: str) -> str:
    messages = [
        {"role": "system", "content": _prompt_title_single},
        {"role": "user", "content": text},
    ]
    response = await aclient.chat.completions.create(model=DEFAULT_MODEL, messages=messages)
    print("Number of input tokens: ", response.usage.prompt_tokens)
    print("Number of output tokens: ", response.usage.completion_tokens)
    output = response.choices[0].message.content
    return output


async def select_title(text: str, titles: List[str]) -> str:
    prompt = load_prompt("select_title").format(titles=titles)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = await aclient.chat.completions.create(model=DEFAULT_MODEL, messages=messages)
    output = response.choices[0].message.content
    return output


async def check_title(text: dict) -> str:
    messages = [
        {"role": "system", "content": _prompt_check_title},
        {"role": "user", "content": text},
    ]
    response = await aclient.chat.completions.create(model=DEFAULT_MODEL, messages=messages)
    output = response.choices[0].message.content
    return output


if __name__ == "__main__":
    title = "Lead Product Designer, 10 years"
    result = asyncio.run(generate_title(text=title))
    print(result)
