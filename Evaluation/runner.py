from typing import Any
from .dataset import load_dataset
from .tasks import TASKS

def evaluate(dataset_path: str, task: str) -> Any:
    df = load_dataset(dataset_path)
    evaluator = TASKS[task]
    summary = evaluator.score(df)
    return summary
