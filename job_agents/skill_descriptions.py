import json
import instructor
from tqdm.asyncio import tqdm
from typing import List
from openai import AsyncOpenAI
import asyncio

"""
- Set the OPENAI_API_KEY environment variable:
    export OPENAI_API_KEY="sk-<your-api-key>"
"""

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())

def make_batches(skills: List[str], batch_size: int) -> List[List[str]]:
    return [skills[i:i+batch_size] for i in range(0, len(skills), batch_size)]

def make_input_content(skills: List[str]) -> str:
    return f"The following skills:\n" +  "\n".join(skills)

async def fetch_response(skills: List[str]) -> str:
    content = make_input_content(skills)

    prompt = f"""You are a HR expert on skill taxonomy.
        You will be provided with a list of skills, and your task is to write a concise, professional 2–3 sentence description for each skill.
        Format as dictionary with keys as skills and values as descriptions."""
    messages = [
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ]

    try:
        response = await aclient.chat.completions.create(
            model=model,
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


async def write_descriptions(skills: List[str], batch_size: int=10) -> dict:
    skill_batches = make_batches(skills, batch_size)
    tasks = [fetch_response(skills) for skills in skill_batches]
    responses = await tqdm.gather(*tasks)
    skill_description_dict = parse_response(responses)
    return skill_description_dict


if __name__ == "__main__":
    skills = [
        "python",
        "machine learning",
        "data analysis",
        "project management",
    ]
    skill_description = asyncio.run(write_descriptions(skills, batch_size=2))
    print(skill_description)