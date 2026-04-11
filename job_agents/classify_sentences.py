from typing import List
from pydantic import BaseModel
from enum import Enum

import asyncio
from .client import aclient, DEFAULT_MODEL, load_prompt


class Labels(Enum):
    COMPANY = "company"
    TASKS = "tasks"
    REQUIREMENTS = "requirements"
    BENEFITS = "benefits"
    OTHERS = "others"


class ClassifiedSentence(BaseModel):
    label: Labels
    sentence: str


prompt = load_prompt("classify_sentences")

async def classify_sentence(sentence: str) -> ClassifiedSentence:
    response = await aclient.beta.chat.completions.parse(
        model=DEFAULT_MODEL,
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