from pathlib import Path
from os.path import join

data_folder = Path(__file__).parent / "data"

catelogue_folder = join(data_folder, "catelogue/")
raw_data_folder = "raw/"
labelled_data_folder = "labeled/"
processed_data_folder = "processed/"