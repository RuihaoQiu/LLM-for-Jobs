"""
This script generates job titles using GPT-3. It uses the OpenAI API to generate job titles based on a list of job descriptions.
"""

import re
import instructor
from tqdm.asyncio import tqdm
from typing import List
from openai import AsyncOpenAI
import pandas as pd
import asyncio

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


async def fetch_response(text: str) -> str:
    prompt = f"""You are a HR and language expert.
        You will be provided with a job description, and your task is to create a proper title for it.
        The title should be simple and clear, neither too general nor too specific, at maximum 4 words."""
    messages = [
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": text
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
        return None