from pathlib import Path
from typing import List, TypeVar, Callable, Awaitable
from tqdm.asyncio import tqdm
from openai import AsyncOpenAI
import instructor

DEFAULT_MODEL = "gpt-4o-mini"
aclient = instructor.patch(AsyncOpenAI())

T = TypeVar("T")


def load_prompt(name: str) -> str:
    return (Path(__file__).parent.parent / "prompts" / f"{name}.txt").read_text()


async def process_in_batches(
    items: List,
    async_func: Callable[..., Awaitable],
    batch_size: int = 10,
    desc: str = "Processing",
) -> List:
    batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    tasks = [async_func(batch) for batch in batches]
    return await tqdm.gather(*tasks, desc=desc)
