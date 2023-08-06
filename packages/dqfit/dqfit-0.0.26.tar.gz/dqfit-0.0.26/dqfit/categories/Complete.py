import pandas as pd
from typing import Any


def fit(fhir_path: pd.DataFrame, context: dict) -> pd.DataFrame:
    def _score_dim(dim: pd.Series) -> int:
        value = dim['value']
        if dim['Conformant'] == 0:
            return None
        elif type(value) == list and len(value) > 0:
            return 1
        elif pd.isna(value):
            return 0
        elif value in ["UNK","unk","","unknown"]:
            return 0
        elif len(str(value)) > 0: # primary case?
            return 1
        else:
            return 0

    fhir_path['Complete'] = fhir_path.apply(_score_dim, axis=1)
    return fhir_path