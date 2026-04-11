import json
import asyncio
from .client import aclient, DEFAULT_MODEL, load_prompt

prompt = load_prompt("extract_skills")


async def extract_skills(job_description: str) -> str:
    response = await aclient.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": job_description},
        ],
        temperature=0.2
    )
    print("Number of input tokens: ", response.usage.prompt_tokens)
    print("Number of output tokens: ", response.usage.completion_tokens)
    output = response.choices[0].message.content
    return json.loads(output)


if __name__ == "__main__":
    input_example = [
        {"input id": "1", "text": "Experience in C/C++."},
        {"input id": "2", "text": "Should know data structures and algorithms."},
    ]

    skills = asyncio.run(extract_skills(job_description=str(input_example)))
    print(skills)
