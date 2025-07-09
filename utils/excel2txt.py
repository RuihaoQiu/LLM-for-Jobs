from pathlib import Path
import pandas as pd

data_path_excel = Path(__file__).parent / ".." / "data/Occupation Data.xlsx"
data_path_txt = Path(__file__).parent / ".." / "data/onet_jobs.txt"

def excel2txt():
    df = pd.read_excel(data_path_excel)
    with open(data_path_txt, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            f.write(f"Title: {row['Title']}\n")
            f.write(f"Description: {row['Description']}\n\n")


if __name__ == "__main__":
    excel2txt()