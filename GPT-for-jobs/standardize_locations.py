from typing import List
from pydantic import BaseModel
from enum import Enum

from openai import AsyncOpenAI
import instructor

aclient = instructor.patch(AsyncOpenAI())


class StandardLocation(BaseModel):
    city: str
    region: str
    country: str


def make_prompt():
    """
    here is just an example, make you own prompt and test it.
    """
    prompt = (
        "You are a geographic expert. "
        "You will be provided a raw text that might include location information. "
        "And you should give back a standard locations including city, region and country. "
        "If there is no city or region, keep it as None. "
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
        response_format=StandardLocation,
    )
    return response
