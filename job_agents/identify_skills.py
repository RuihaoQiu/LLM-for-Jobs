import asyncio
from .client import aclient, DEFAULT_MODEL, load_prompt

prompt = load_prompt("identify_skills")


async def extract_skills(context: str, skill: str) -> str:
    response = await aclient.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": f"context: {context}\nskill: {skill}"},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    description = "We are looking for a software engineer with experience in Python and ML."
    skill = "Machine learning"
    is_skill = asyncio.run(extract_skills(context=description, skill=skill))
    print(is_skill)
