import asyncio
from agents import Agent, Runner


async def main():
    agent = Agent(name="Assistant", instructions="You are an expert of job and skill catelogue.")

    result = await Runner.run(agent, "Recommend 5 most relevant titles from ONet.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.

if __name__ == "__main__":
    asyncio.run(main())