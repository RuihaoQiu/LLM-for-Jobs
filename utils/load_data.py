from pathlib import Path
from typing import List
import pandas as pd
import json

_root = Path(__file__).parent.parent
data_path_excel = _root / "data/Occupation Data.xlsx"
data_path_txt = _root / "data/onet_jobs.txt"
prompts_path = _root / "data/prompts.json"


def excel2txt():
    df = pd.read_excel(data_path_excel)
    with open(data_path_txt, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            f.write(f"Title: {row['Title']}\n")
            f.write(f"Description: {row['Description']}\n\n")


def load_prompts():
    with open(prompts_path, 'r') as f:
        data = json.load(f)
    return data


def get_csv_files(folder: Path) -> List[Path]:
    return [f for f in folder.iterdir() if f.is_file() and f.suffix == ".csv"]


def read_csv_files(files: List[Path]) -> List[pd.DataFrame]:
    return [pd.read_csv(f) for f in files]


def load_raw_data(raw_data_folder: Path) -> pd.DataFrame:
    csv_files = get_csv_files(raw_data_folder)
    dataframes = read_csv_files(csv_files)
    return pd.concat(dataframes, ignore_index=True)


if __name__ == "__main__":
    print(load_prompts())