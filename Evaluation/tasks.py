from abc import ABC, abstractmethod
from os import path
from typing import Dict
import pandas as pd
from .dataset import load_dataset
from .metrics import accuracy, precision_recall_f1

project_folder = path.join(path.dirname(__file__), '..')
gold_data_folder = path.join(project_folder, "data", "gold")


class EvaluationTask(ABC):
    name: str

    @abstractmethod
    def score(self, df_pred: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Score predictions against gold data. Returns {column: {metric: value}}."""


class SkillsEvaluation(EvaluationTask):
    name = "skills_evaluation"

    def __init__(self):
        self.df_gold = load_dataset(path.join(gold_data_folder, "skills_gold.csv"))
        print(f"Loaded {len(self.df_gold)} gold samples for skills evaluation.")

    def score(self, df_pred: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        summary = {}
        for column in self.df_gold.columns:
            gold = self.df_gold[column].tolist()
            preds = df_pred[column].fillna("").astype(str).tolist()
            summary[column] = {
                "accuracy": accuracy(gold, preds),
                **precision_recall_f1(gold, preds),
            }
        return summary


class TitleEvaluation(EvaluationTask):
    name = "title_evaluation"

    def __init__(self):
        self.df_gold = load_dataset(path.join(gold_data_folder, "title_gold.csv"))
        print(f"Loaded {len(self.df_gold)} gold samples for title evaluation.")

    def score(self, df_pred: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        summary = {}
        for column in self.df_gold.columns:
            gold = self.df_gold[column].tolist()
            preds = df_pred[column].fillna("").astype(str).tolist()
            summary[column] = {
                "accuracy": accuracy(gold, preds),
                **precision_recall_f1(gold, preds),
            }
        return summary


class SalaryEvaluation(EvaluationTask):
    name = "salary_evaluation"

    def __init__(self):
        self.df_gold = load_dataset(path.join(gold_data_folder, "salary_gold.csv"))
        print(f"Loaded {len(self.df_gold)} gold samples for salary evaluation.")

    def score(self, df_pred: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        summary = {}
        for column in self.df_gold.columns:
            df_pred[column] = df_pred[column].fillna(-1)
            gold = self.df_gold[column].tolist()
            preds = df_pred[column].tolist()
            summary[column] = {"accuracy": accuracy(gold, preds)}
        return summary


# Task registry — instantiated lazily to avoid loading gold files on import
_TASK_CLASSES = {
    "salary": SalaryEvaluation,
    "skills": SkillsEvaluation,
    "title": TitleEvaluation,
}
_task_instances: Dict[str, EvaluationTask] = {}


def get_task(name: str) -> EvaluationTask:
    if name not in _TASK_CLASSES:
        raise KeyError(f"Unknown task '{name}'. Available: {list(_TASK_CLASSES)}")
    if name not in _task_instances:
        _task_instances[name] = _TASK_CLASSES[name]()
    return _task_instances[name]


# Keep TASKS as a convenience alias for backward compatibility
class _LazyTaskRegistry:
    def __getitem__(self, key: str) -> EvaluationTask:
        return get_task(key)


TASKS = _LazyTaskRegistry()
