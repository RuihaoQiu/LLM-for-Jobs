from pydantic import BaseModel

from openai import AsyncOpenAI
import instructor
import asyncio

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
        "If there is no city, region or country, keep it as None. "
    )
    return prompt


async def standardize_location(raw_location: str) -> StandardLocation:
    prompt = make_prompt()
    response = await aclient.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": raw_location},
        ],
        response_format=StandardLocation,
    )
    return response.choices[0].message.parsed


async def standardize_locations(locations: list[str]) -> list[StandardLocation]:
    tasks = [standardize_location(location) for location in locations]
    standardized_locations = await asyncio.gather(*tasks)
    return standardized_locations


if __name__ == "__main__":
    # Example usage
    raw_location = "Beijing, Beijing, CN"
    standardized_location = asyncio.run(standardize_location(raw_location))
    print(standardized_location)