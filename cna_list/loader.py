import os
import json

from tqdm import tqdm

from pathlib import Path
from cna_list.models import CNA


def get_external_path():
    path = os.getenv("CNA_DATA_PATH")

    if not path:
        raise FileNotFoundError("CNA_DATA_PATH not set")

    path = Path(path).expanduser()

    if not path.exists():
        raise FileNotFoundError("External data directory not found")

    return path


class CNALoader:
    def __init__(self, path: Path = None):
        # if path is not provided, load from package or external dir
        if path:
            # check if the CNA data path exists
            self.path = Path(path).expanduser()

            if not self.path.exists():
                raise FileNotFoundError(f"{path} not found")
        else:
            print("Path not provided. Loading CNA data from external path")
            self.path = get_external_path()

        self.records = {}

        for cna_file in tqdm(self.path.iterdir(), desc="Loading CNA data", unit='file'):
            cna = self.load(cna_file)
            self.records[cna.email] = cna

    @staticmethod
    def load(file_path: Path):
        if not file_path.exists():
            # Raise an error if the file is not found in both locations
            raise FileNotFoundError(f"No such file: '{file_path}'.")

        print(f"Loading CNA from data path: {file_path}")

        with file_path.open('r') as file:
            data = json.load(file)

        # Validate the loaded data against the CNA model
        cna = CNA(**data)

        return cna

    @staticmethod
    def load_from_external(file_name: str):
        path = get_external_path()

        return CNALoader.load(path / file_name)

    def __getitem__(self, key):
        return self.records[key]
