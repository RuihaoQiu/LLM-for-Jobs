from typing import List, Dict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def accuracy(gold: List[str], preds: List[str]) -> float:
    return accuracy_score(gold, preds)


def precision_recall_f1(gold: List[str], preds: List[str], average: str = "weighted") -> Dict[str, float]:
    precision, recall, f1, _ = precision_recall_fscore_support(gold, preds, average=average, zero_division=0)
    return {"precision": precision, "recall": recall, "f1": f1}
