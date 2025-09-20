from openai import AsyncOpenAI
import instructor
import asyncio

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


prompt = """
You are an expert in skill taxonomy.
You will be given a sentence from job description. Your task is to extract a list of skills.

Extraction Rules
Extract skills from the tasks, requirements, and qualifications mentioned in the job description.

Skill Fields:
Each extracted skill must include:
name: the normalized skill name.
span: the exact text span of the skill as it appears in the sentence.

Formatting Rules:
Extract as many valid skills as possible.
Do not include adjectives (e.g., excellent, strong, good, advanced, proficient) in the name or span.
The span must exactly match the wording in the job description.
The name may differ from the span but must be a valid skill (not too general or too specific).
The name should be in Title Case and noun form (e.g., "Python", "Project Management"), transform verbs to nouns (e.g., "Collaboration" instead of "Collaborate").
IF there is no skill in the input, return None.

Output

Return only valid JSON, with no explanations or extra text.
Format:

[
  {
    "name": "Python",
    "span": "Python"
  }
]

"""


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
        temperature=0.2
    )
    print("Number of input tokens: ", response.usage.prompt_tokens)
    print("Number of output tokens: ", response.usage.completion_tokens)
    return response.choices[0].message.content


if __name__ == "__main__":
    description = """
  When you apply, a Cisco representative may contact you directly if a relevant position opens. 
    """
    skills = asyncio.run(extract_skills(job_description=description))
    print(skills)
