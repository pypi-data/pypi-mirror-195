import pandas as pd
from dqfit.services import ContextManager

def fit(fhir_path: pd.DataFrame, context_key: str) -> pd.DataFrame:
    """Takes in fhir_path, returns fhir_path with added vector"""
    context = ContextManager.load_context(context_key)
    def _score_dim(dim: pd.Series) -> int:
        path  = dim['path']
        if path in context['path']:
            return 1
        else:
            return 0
    fhir_path['Conformant'] = fhir_path.apply(_score_dim, axis=1)
    return fhir_path
    