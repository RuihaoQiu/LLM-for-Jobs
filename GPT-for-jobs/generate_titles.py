"""
This script generates job titles using GPT-3. It uses the OpenAI API to generate job titles based on a list of job descriptions.
"""
import instructor
from typing import List
from openai import AsyncOpenAI

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())

async def generate_title(text: str) -> str:
    prompt = f"""You are a HR and language expert.
        You will be provided with a job description, and your task is to create a proper title for it.
        The title should be simple and clear, neither too general nor too specific, at maximum 4 words."""
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]

    try:
        response = await aclient.chat.completions.create(model=model, messages=messages)
        output = response.choices[0].message.content
        return output
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        return None


async def select_title(text: str, titles: List[str]) -> str:
    prompt = f"""You are a HR and language expert.
        You will be provided with a job description, and your task is to select a proper title from the provided list: {titles}.
        If there is no proper title, just return None."""
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]

    try:
        response = await aclient.chat.completions.create(model=model, messages=messages)
        output = response.choices[0].message.content
        return output
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        return None
