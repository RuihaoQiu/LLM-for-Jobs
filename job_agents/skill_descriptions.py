import json
from typing import List
import asyncio
from .client import aclient, DEFAULT_MODEL, process_in_batches, load_prompt

_prompt = load_prompt("skill_descriptions")

def make_input_content(skills: List[str]) -> str:
    return f"The following skills:\n" +  "\n".join(skills)

async def fetch_response(skills: List[str]) -> str:
    content = make_input_content(skills)
    messages = [
        {"role": "system", "content": _prompt},
        {"role": "user", "content": content},
    ]

    try:
        response = await aclient.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages
        )
        output = response.choices[0].message.content
        return output
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        return ""

def parse_response(responses: str) -> dict:
    result_dict = {}
    for response in responses:
        try:
            result_dict = result_dict | json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
    return result_dict


async def write_descriptions(skills: List[str], batch_size: int = 10) -> dict:
    responses = await process_in_batches(skills, fetch_response, batch_size, desc="Writing descriptions")
    return parse_response(responses)


if __name__ == "__main__":
    skills = [
        "python",
        "machine learning",
        "data analysis",
        "project management",
    ]
    skill_description = asyncio.run(write_descriptions(skills, batch_size=2))
    print(skill_description)