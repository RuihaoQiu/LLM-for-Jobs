from os import path
from typing import Dict
import pandas as pd
from dataset import load_dataset
from sklearn.metrics import accuracy_score

project_folder = path.join(path.dirname(__file__), '..')
gold_data_folder = path.join(project_folder, "data", "gold")


class SkillsEvaluation():
    name = "salary_evaluation"
    def __init__(self):
        self.df_gold = load_dataset(path.join(gold_data_folder, "skills_gold.csv"))
        print(f"Loaded {len(self.df_gold)} gold samples for skills evaluation.")

    def score(self, df_pred: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        summary = {}
        return summary

class TitleEvaluation():
    name = "title_evaluation"
    def __init__(self):
        self.df_gold = load_dataset(path.join(gold_data_folder, "title_gold.csv"))
        print(f"Loaded {len(self.df_gold)} gold samples for title evaluation.")

    def score(self, df_pred: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        summary = {}
        return summary

class SalaryEvaluation():
    name = "salary_evaluation"
    def __init__(self):
        self.df_gold = load_dataset(path.join(gold_data_folder, "salary_gold.csv"))
        print(f"Loaded {len(self.df_gold)} gold samples for salary evaluation.")

    def score(self, df_pred: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        summary = {}
        for column in self.df_gold.columns:
            df_pred[column] = df_pred[column].fillna(-1)
            summary[column] = {}
            summary[column]["accuracy"] = accuracy_score(self.df_gold[column], df_pred[column])
        return summary


# Task registry
TASKS = {
    "salary": SalaryEvaluation(),
}