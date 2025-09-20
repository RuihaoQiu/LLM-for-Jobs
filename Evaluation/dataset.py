import pandas as pd

def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["min_salary"] = df["min_salary"].fillna(-1).astype(int).astype(str)
    df["max_salary"] = df["max_salary"].fillna(-1).astype(int).astype(str)
    df["currency"] = df["currency"].fillna("N/A")
    df["period"] = df["period"].fillna("N/A")
    return df