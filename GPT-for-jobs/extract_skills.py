from openai import AsyncOpenAI
import instructor
import asyncio

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


prompt = (
    "You are an expert in skill taxonomy. You will provide you a job description "
    "and you extract a list of skills from it. The skills should be precise and less than 3 words. "
)


async def extract_skills(job_description: str) -> str:
    response = await aclient.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": job_description},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    description = "We are looking for a software engineer with experience in Python and machine learning."
    skills = asyncio.run(extract_skills(job_description=description))
    print(skills)
