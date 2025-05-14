from load_data import load_raw_data
from job_agents.classify_sentences import classify_sentences

def label_data(input_file: str, output_file: str) -> None:
    df = load_raw_data()
    asyncio.run(classify_sentences(job))

