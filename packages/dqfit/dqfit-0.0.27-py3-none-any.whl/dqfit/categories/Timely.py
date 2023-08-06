import pandas as pd


def _date_scalar_query():
    df = pd.DataFrame(
        dict(_date=pd.date_range(start="2016-01-01", end="today"))
    ).reset_index()
    df["index"] = df["index"] / df["index"].max()
    df = df.rename(columns={"index": "Timely"})
    return df


DATE_SCALAR = _date_scalar_query()

DATETIME_PATHS = [
    "Procedure.performed[x]",
    "Condition.onset[x]",
    "Patient.birthDate",
    "Observation.effective[x]",
]


def score(fhir_path: pd.DataFrame, context: dict) -> pd.DataFrame:
    # todo handle date range from Context
    df = fhir_path
    df = df[df["path"].isin(DATETIME_PATHS)].reset_index(drop=True)
    df["_date"] = df["value"].apply(lambda x: str(x)[0:10])
    df["_date"] = pd.to_datetime(df["_date"], errors='coerce')
    df = df.merge(DATE_SCALAR, how="left")
    fhir_path = fhir_path.merge(
        df[["id", "Timely","_date"]], how="left", left_on="id", right_on="id"
    )
    # fhir_path['timely'] = fhir_path['timely'].fillna(0) # hmmm this aint it. maybe drop em?
    return fhir_path
