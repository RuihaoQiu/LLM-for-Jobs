from pydantic import BaseModel
import asyncio
from .client import aclient, DEFAULT_MODEL, load_prompt

_prompt = load_prompt("standardize_locations")


class StandardLocation(BaseModel):
    city: str
    region: str
    country: str


async def standardize_location(raw_location: str) -> StandardLocation:
    response = await aclient.beta.chat.completions.parse(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": _prompt,
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
    location = "Beijing, Beijing, CN"
    standardized_location = asyncio.run(standardize_location(raw_location=location))
    print(standardized_location)
