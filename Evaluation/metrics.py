from typing import List, Tuple

def accuracy(gold: List[str], preds: List[str]) -> float:
    return sum(p == g for p, g in zip(preds, gold)) / len(gold)