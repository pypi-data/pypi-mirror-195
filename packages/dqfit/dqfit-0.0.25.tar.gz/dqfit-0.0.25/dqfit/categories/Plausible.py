import pandas as pd
from typing import Any
from pathlib import Path
from dqfit.services import ContextManager

package_dir = Path(__file__).parent.parent

MIN_DATE = "1900-01-01"
TODAY_ISO = str(pd.to_datetime("today"))[0:10]

DATETIME_PATHS = [
    "Procedure.performed[x]",
    "Condition.onset[x]",
    "Condition.abatement[x]",
    "Condition.recordedDate",
    "Patient.birthDate",
    "Observation.effective[x]",
    "MedicationDispense.whenHandedOver"
]

DISCRETE_SETS = {
    "Procedure.status": [
        "preparation",
        "in-progress",
        "not-done",
        "on-hold",
        "stopped",
        "completed",
        "entered-in-error",
        "unknown",
    ],
    "Observation.status": ["final", "registered", "preliminary", "amended"],
    "Condition.clinicalStatus": [
        "active",
        "recurrence",
        "relapse",
        "inactive",
        "remission",
        "resolved",
    ],
    "Patient.gender": ["male", "female", "other", "unknown"],
    "Coding.system": [
        "http://snomed.info/sct",
        "http://hl7.org/fhir/sid/icd-9-cm",
        "http://hl7.org/fhir/sid/icd-10-cm",
        "http://loinc.org",
        "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
        "http://www.ama-assn.org/go/cpt",
        "http://www.nlm.nih.gov/research/umls/rxnorm",
        "http://hl7.org/fhir/sid/ndc",
    ]
}

# "https://build.fhir.org/valueset-coverage-type.html"

def _plausible_period_score(period: dict):
    # DRAFT
    score = 0
    if "start" in period.keys():
        score += _plausible_dt_score(period["start"]) / 2
    if "end" in period.keys():
        yr = int(period["end"][0:4])
        if yr <= 2024:
            score += 0.5
    return score


def _plausible_dt_score(dt: str) -> int:
    if pd.isna(dt):
        return 0
    date = dt[0:10]
    if MIN_DATE < date <= TODAY_ISO:
        return 1
    else:
        return 0


def _plausible_discrete_score(fhir_path: str, value: Any) -> int:
    "For in range"
    # this could use a better name
    if value in DISCRETE_SETS[fhir_path]:
        return 1
    else:
        return 0


def _plausible_codeable_concept_score(codeable_concept, context: dict):
    # {
    #     "coding": [{"system": "http://loinc.org", "code": "4548-4"}]
    # }
    score = 0
    if "coding" in codeable_concept.keys():
        score += 0.1
    coding: list = codeable_concept.get("coding", [])
    for coding in coding:
        if coding["system"] in DISCRETE_SETS["Coding.system"]:
            score += 0.4
        if coding["code"] in context["code"]:
            score += 0.5
    return min(score, 1)


def _plausible_type_score(type: dict):
    #
    if "coding" in type.keys():
        return 1
    else:
        return 0

def _plausible_subject_score(subject: dict):
    #
    score = 0
    if type(subject) != dict:
        return 0
    elif "reference" in subject.keys():
        return 1
    else:
        return 0


def _plausible_clinical_status_score(clinical_status: dict):
    #
    if "coding" in clinical_status.keys():
        return 1
    else:
        return 0


def fit(fhir_path: pd.DataFrame, context_key: str) -> pd.DataFrame:
    context = ContextManager.load_context(context_key)

    def _score_dim(dim: pd.Series):
        fhir_path = dim["path"]
        value = dim["value"]
        if dim["Complete"] in [None, 0]:
            return None
        elif fhir_path in DATETIME_PATHS:
            if type(value) == str:
                return _plausible_dt_score(value)
            elif type(value) == dict:
                return _plausible_period_score(value)
        elif fhir_path in DISCRETE_SETS.keys():
            return _plausible_discrete_score(fhir_path, value)
        elif fhir_path.endswith(".code"):
            # todo handle medicationCodeableConcept
            return _plausible_codeable_concept_score(value, context)
        elif fhir_path.endswith(".subject"):
            return _plausible_subject_score(value)
        elif fhir_path.endswith(".period"):
            return _plausible_period_score(value)
        elif fhir_path == "Coverage.type":
            return _plausible_codeable_concept_score(value, context)
        elif fhir_path.endswith(".clinicalStatus"):
            return _plausible_clinical_status_score(value)

    fhir_path["Plausible"] = fhir_path.apply(_score_dim, axis=1)
    return fhir_path
