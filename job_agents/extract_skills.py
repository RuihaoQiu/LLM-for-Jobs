import json
from openai import AsyncOpenAI
import instructor
import asyncio

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


prompt = """
You are an expert in skill taxonomy.
You will be given a list of sentences (each with an input id) from a job description.
Your task is to extract a list of skills.

Skill Fields

Each extracted skill object must include:
input id: copy exactly from the input, do not modify.
name: the normalized skill name.
span: the exact text span of the skill as it appears in the sentence.

Extraction Rules

Extract skills only from tasks, requirements, and qualifications.
Extract as many valid skills as possible from each sentences, certain sentence might have multiple skills.
Do not include adjectives such as excellent, strong, good, advanced, proficient.
The name may differ from the span, but must be a valid skill: 
    - Use Title Case; 
    - Use noun form (e.g., "Collaboration" instead of "collaborate"); 
    - Avoid names that are too general or too specific.
If a sentence contains no skill, ignore it.

Output Rules

Output only a valid JSON array of skill objects.
No explanations, no extra text.


Example

Input

[
  {"input id": "1", "text": "Experience in Python and machine learning."},
  {"input id": "2", "text": "Should have a degree in Computer Science."}
]


Output

[
  {
    "input id": "1",
    "name": "Python",
    "span": "Python"
  },
  {
    "input id": "1",
    "name": "Machine Learning",
    "span": "machine learning"
  },
  {
    "input id": "2",
    "name": "Computer Science",
    "span": "Computer Science"
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
    output = response.choices[0].message.content
    return json.loads(output)


if __name__ == "__main__":
    input_example = [
        {"input id": "1", "text": "Experience in C/C++."},
        {"input id": "2", "text": "Should know data structures and algorithms."},
    ]

    skills = asyncio.run(extract_skills(job_description=str(input_example)))
    print(skills)
