import re
import instructor
from tqdm.asyncio import tqdm
from typing import List
from openai import AsyncOpenAI
import pandas as pd
import asyncio

"""
- Set the OPENAI_API_KEY environment variable:
    export OPENAI_API_KEY="sk-<your-api-key>"
"""

model = "gpt-4o-mini"
numerical_regex = re.compile(r"^\d+[\.]?\s*")
aclient = instructor.patch(AsyncOpenAI())

def make_batches(titles: List[str], batch_size: int) -> List[List[str]]:
    return [titles[i:i+batch_size] for i in range(0, len(titles), batch_size)]

def rm_newlines(title: str) -> str:
    return re.sub(r"\n+", " ", title)

def make_input_content(titles: List[str]) -> str:
    return "\n".join([f"{i+1}. "+ rm_newlines(title) for i, title in enumerate(titles)])

async def fetch_response(titles: List[str]) -> str:
    content = make_input_content(titles)
    prompt = f"""You are a HR and language expert.
        You will be provided with a numerical list of job titles, and your task is to translate them into English.
        The output should be a numerical list of translated titles separated by newline."""
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
        return None

def remove_numerical(title: str) -> str:
    return numerical_regex.sub("", title).strip()

def process_output_content(content: str) -> List[str]:
    titles = content.split("\n")
    return [remove_numerical(title) for title in titles]

def get_titles(contents: List[str]) -> List[str]:
    return [title for content in contents for title in process_output_content(content)]

async def translate_titles(titles: List[str], batch_size: int=10) -> List[str]:
    title_batches = make_batches(titles, batch_size)
    tasks = [fetch_response(titles) for titles in title_batches]
    responses = await tqdm.gather(*tasks)
    titles = get_titles(responses)
    return titles


if __name__ == "__main__":
    df = pd.read_parquet("data/inputs/LT-1.parquet")
    all_titles = df["job_title"].to_list()[:200]
    translated_titles = asyncio.run(translate_titles(all_titles))
    print(translated_titles)