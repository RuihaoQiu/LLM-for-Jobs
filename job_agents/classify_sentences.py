from typing import List
from pydantic import BaseModel
from enum import Enum

import asyncio
from openai import AsyncOpenAI
import instructor

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


class Labels(Enum):
    COMPANY = "company"
    TASKS = "tasks"
    REQUIREMENTS = "requirements"
    BENEFITS = "benefits"
    OTHERS = "others"


class ClassifiedSentence(BaseModel):
    label: Labels
    sentence: str


prompt = (
        "You are a HR expert for job posts. You will be provided a sentence or paragraph from ajob description "
        "and you should give back a label. The label should be one of the following: "
        f"{', '.join([label.value for label in Labels])}. "
        'The "company" category is about company description, what the company does in general; '
        "tasks are about what an employee's daily tasks are and what they have to do; "
        "requirements are about what qualifications a potential employee must have; "
        "benefits are all types of perks and rewards for working in the company; "
        "if the sentence or paragraph does not fit any of these categories, label it as 'others'. "
)

async def classify_sentence(sentence: str) -> ClassifiedSentence:
    response = await aclient.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": sentence},
        ],
        response_format=ClassifiedSentence,
    )
    return response.choices[0].message.parsed

if __name__ == "__main__":
    sentences = [
        "We are looking for a software engineer with experience in Python and machine learning. ",
        "The company is a leading tech firm specializing in AI solutions. ",
        "The ideal candidate should have a degree in Computer Science and at least 3 years of experience. ",
        "We offer competitive salaries and flexible working hours.",
        "Contact us for more information.",
    ]
    for s in sentences:
        classified_sentence = asyncio.run(classify_sentence(sentence=s))
        print(classified_sentence)