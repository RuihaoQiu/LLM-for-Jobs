import asyncio
from agents import Agent, Runner
from utils.load_data import load_prompts

prompts = load_prompts()
print(prompts)

agent = Agent(name="Assistant", instructions="You are an expert of job and skill catelogue.")

async def recommend_titles(input_title: str):
    result = await Runner.run(agent, f"Recommend 5 most relevant titles from ONet.  Here is my input title is {input_title}")
    print(result.final_output)

if __name__ == "__main__":
    title = "machine learning engineer"
    # asyncio.run(recommend_titles(title))