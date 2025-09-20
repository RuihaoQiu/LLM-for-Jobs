import json
import instructor
from typing import List
from openai import AsyncOpenAI
import asyncio

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


async def generate_titles(titles: List) -> tuple:
    prompt = """You are an HR expert.
You will be given a list of raw job titles from online job posts. 
Your task is to create the corresponding standardized titles, each title title includes the following items and rules:

Rules

title id:
The same as the input title id, do not modify it.

raw title:
The original job title as it appears exactly in the input. Do not modify it.

title name:
- Use Title Case (e.g., "Software Engineer", "Data Scientist").
- Keep it simple, clear, and no longer than 4 words.
- Avoid being too general or too specific.
- Avoid using seniority terms in the title name.

span:
The exact text span of the title as it appears in the raw job title.

seniority:
- One of: "Intern", "Junior", "Mid", "Senior", "Lead", "Director".
- If no seniority information is present, use "None".

Additional Instructions
for each raw title, if there are multiple titles in the raw input, return the most relevant one.

For example, given the input:
[
    {
    "id": "123", 
    "raw title": "Software Engineer II, manager"
    },
    {
    "id": "124",
    "raw title": "Senior Data Scientist"
    }
]

Output only valid JSON in the following format:
[
{
    "id": "123",
    "raw title": "Software Engineer II, manager",
    "title name": "Software Engineer",
    "span": "Software Engineer",
    "seniority": "Lead"
},
{
    "id": "124",
    "raw title": "Senior Data Scientist",
    "title name": "Data Scientist",
    "span": "Data Scientist",
    "seniority": "Senior"
}
]

"""
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": titles},
    ]
    response = await aclient.chat.completions.create(model=model, messages=messages)
    token_counts = (response.usage.prompt_tokens, response.usage.completion_tokens)
    print("Number of input tokens: ", response.usage.prompt_tokens)
    print("Number of output tokens: ", response.usage.completion_tokens)
    output = response.choices[0].message.content
    return json.loads(output), token_counts


async def generate_title(text: str) -> str:
    prompt = """You are an HR and language expert.
You will be given a raw job title from an online job post. 
Your task is to create a standardized title including following items and rules:

Rules

raw title:
The original job title as it appears in the job post.

title name:
- Use Title Case (e.g., "Software Engineer", "Data Scientist").
- Keep it simple, clear, and no longer than 4 words.
- Avoid being too general or too specific.

span:
The exact text span of the title as it appears in the raw job title.

seniority:
- One of: "Intern", "Junior", "Mid", "Senior", "Lead", "Director".
- If no seniority information is present, use "None".

Additional Instructions
If there are multiple titles in the raw input, return the most relevant one.
Output only valid JSON in the following format:
{
    "raw title": "Software Engineer II",
    "title name": "Software Engineer",
    "span": "Software Engineer",
    "seniority": "Mid"
}
"""
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = await aclient.chat.completions.create(model=model, messages=messages)
    print("Number of input tokens: ", response.usage.prompt_tokens)
    print("Number of output tokens: ", response.usage.completion_tokens)
    output = response.choices[0].message.content
    return output


async def select_title(text: str, titles: List[str]) -> str:
    prompt = f"""You are a HR and language expert.
        You will be provided with a job description, and your task is to select a proper title from the provided list: {titles}.
        If there is no proper title, just return None."""
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = await aclient.chat.completions.create(model=model, messages=messages)
    output = response.choices[0].message.content
    return output


async def check_title(text: dict) -> str:
    prompt = f"""You are an HR and language expert.
    You will be given two inputs:
    
    A job title from an online job portal.
    A standard title from the internal taxonomy.
    
    Instructions:
    
    Step 1: Check if the job portal title matches the standard taxonomy title.
    Step 2:
    If it matches, return the standard title.
    If it does not match, generate the most appropriate standardized title.
    
    The output should only be the final title, with no explanations or extra text.
"""
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = await aclient.chat.completions.create(model=model, messages=messages)
    output = response.choices[0].message.content
    return output



if __name__ == "__main__":
    title = "Lead Product Designer, 10 years"
    result = asyncio.run(generate_title(text=title))
    print(result)