from job_agents.classify_sentences import classify_sentences

def label_data(input_file: str, output_file: str) -> None:
    classify_sentences(input_file, output_file)

