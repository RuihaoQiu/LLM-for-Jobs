from typing import List
from pydantic import BaseModel
from enum import Enum

from openai import AsyncOpenAI
import instructor

model = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())


class Labels(Enum):
    COMPANY = "company"
    TASKS = "tasks"
    REQUIREMENTS = "requirements"
    BENEFITS = "benefits"


class ClassifiedJobParagraph(BaseModel):
    label: Labels
    paragraph: str


prompt = (
        "You are a segmenter for job descriptions. I will provide you a job description "
        "and you should give back a list of sections. The output should be in utf-8. "
        "Some parts of the description might be omitted if they do not fit into any category, and there might be cases where "
        "no info on a category can be found. Try to avoid having the same sentences in "
        'different paragraphs. The "company" category is about company description and '
        "what the company does in general; tasks are about what an employee's "
        "responsibilities are and what they have to do; requirements are about what "
        "qualifications a potential employee must have; benefits are all types of "
        "perks and rewards for working in the company. A job description must "
        "contain no more than one paragraph per category - if new info is found, "
        "add it to the existing paragraph where it fits best."
)

async def classify_job_description(job_description: str) -> List[ClassifiedJobParagraph]:
    response = await aclient.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": job_description},
        ],
        response_format=List[ClassifiedJobParagraph],
    )
    return response
