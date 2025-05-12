import pandas as pd
from src.config import data_folder


def load_raw_data() -> pd.DataFrame:
    dfs = []
    raw_data_path = data_folder / "raw_data"
    for file in raw_data_path.iterdir():
        if file.is_file() and file.suffix == ".csv":
            file_path = raw_data_path / file
            df_batch = pd.read_csv(file_path)
            dfs.append(df_batch)
    df = pd.concat(dfs, ignore_index=True)
    return df