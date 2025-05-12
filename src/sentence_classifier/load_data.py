import pandas as pd
from pathlib import Path
from typing import List
from src.config import data_folder

def get_csv_files(folder: Path) -> List[Path]:
    return [file for file in folder.iterdir() if file.is_file() and file.suffix == ".csv"]

def read_csv_files(files: List[Path]) -> List[pd.DataFrame]:
    return [pd.read_csv(file) for file in files]

def load_raw_data() -> pd.DataFrame:
    raw_data_path = data_folder / "raw_data"
    csv_files = get_csv_files(raw_data_path)
    dataframes = read_csv_files(csv_files)
    return pd.concat(dataframes, ignore_index=True)