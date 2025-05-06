from openai import AsyncOpenAI
import instructor
import asyncio

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


prompt = (
    "You are an expert in skill taxonomy. You will provide you a sentence/contex and a potential skill, "
    "and you will identify whether the skill is in the context. "
    "just return True or False. "
)


async def extract_skills(context: str, skill: str) -> str:
    response = await aclient.chat.completions.create(
        model=model,
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
