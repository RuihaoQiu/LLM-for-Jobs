from typing import List
from pydantic import BaseModel
from enum import Enum

from openai import AsyncOpenAI
import instructor

aclient = instructor.patch(AsyncOpenAI())


class StandardLocation(BaseModel):
    city: str
    county: str
    country: str


def make_prompt():
    """
    here is just an example, make you own prompt and test it.
    """
    prompt = (
        "You are a geographic expert. "
        "You will be provided a raw text that might include location information. "
        "And you should give back a list of standard locations including city, county and country. "
        "If there is no city or county, keep it as None. "
    )
    return prompt


async def standardize_location(raw_location: str) -> List[StandardLocation]:
    prompt = make_prompt()
    response = await aclient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": raw_location},
        ],
        max_retries=5,
        response_format=List[StandardLocation],
    )
    return response
