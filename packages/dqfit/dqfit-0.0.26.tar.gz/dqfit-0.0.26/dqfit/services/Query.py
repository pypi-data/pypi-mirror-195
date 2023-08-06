import random
import json
import gzip
from pathlib import Path
import pandas as pd

from glob import glob
from tqdm import tqdm

PACKAGE_DIR = Path(__file__).parent.parent

def _load_bundle(path):
    # json loads kinda costly
    # consider going to msgspec to esure entry
    if path.endswith('.json.gz'):
        with gzip.open(path, "r") as f:
            bundle = json.loads(f.read())
    elif path.endswith('.json'):
        with open(path, "r") as f:
            bundle = json.loads(f.read())
    else: 
        print("not a .json or .json.gz")
        
    if pd.isna(bundle):
        print(path, 'is null')
        return {}
    
    return bundle

def bundles_query(srcdir: str, limit=-1, offset=0) -> pd.DataFrame:
    """
    Takes in a srcdir containing FHIR bundles
    adds concept of bundle_index (i.e. where was it in the list) for PMI
    ensures / overwrites 'total'
    Returns Bundles in a DataFrame.
    """
    if "synthea_10" in srcdir:
        srcdir = f"{PACKAGE_DIR}/data/synthetic/synthea_10"
    paths = glob(f"{srcdir}/*")
    if limit > 0:
        paths = paths[offset:(offset+limit)]
    bundles = pd.DataFrame([_load_bundle(p) for p in tqdm(paths)])
    bundles = bundles.dropna(subset=['entry']) # if doesnt have entry...
    bundles = bundles.reset_index().rename(columns={"index": "bundle_index"})
    bundles["total"] = bundles["entry"].apply(lambda x: len(x))
    assert "bundle_index" in bundles.columns
    return bundles


def bundles_sample_query(srcdir: str, k: int, offset=0) -> pd.DataFrame:
    assert(k > 0)
    paths = glob(f"{srcdir}/*")
    print(f"Sampling {k} of {len(paths)} bundles {(100*k/len(paths)):2f}%")
    paths = random.choices(paths, k=k)
    bundles = pd.DataFrame([_load_bundle(p) for p in tqdm(paths)])
    bundles = bundles.dropna(subset=['entry']) # if doesnt have entry...
    bundles = bundles.reset_index().rename(columns={"index": "bundle_index"})
    bundles["total"] = bundles["entry"].apply(lambda x: len(x))
    assert "bundle_index" in bundles.columns
    return bundles


## clean up belwo 


def valueset_query(oid: str) -> pd.DataFrame:
    """
    Query OID from package data
    """

    def _get_vs(oid: str) -> dict:
        vs_path = f"{PACKAGE_DIR}/data/valuesets/{oid}.json"
        with open(vs_path, "r") as f:
            vs = json.load(f)
        return vs

    return pd.DataFrame([_get_vs(oid)])


def context_path_query(context_key: str) -> pd.DataFrame:
    with open(f"{PACKAGE_DIR}/data/contexts.json", "r") as f:
        contexts = json.load(f)
    return pd.DataFrame(dict(path=contexts[context_key]["path"]))


def context_code_query(context_key: str) -> pd.DataFrame:
    with open(f"{PACKAGE_DIR}/data/contexts.json", "r") as f:
        contexts = json.load(f)
    return pd.DataFrame(dict(code=contexts[context_key]["code"]))


def ig_struct_query(
    resource_types: list = [],
    must_support=False,
) -> pd.DataFrame:
    """
    Point at a directory of fhir struct defitition directory
    And the relavent resource_types
    Returns the path, datatypes
    """
    def _struct_element_snapshot_query(struct_path: str) -> pd.DataFrame:
        with open(struct_path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data["snapshot"]["element"])
        df["_file"] = struct_path
        return df
    structs_dir = f"{PACKAGE_DIR}/data/structs"
    struct_paths = glob(f"{structs_dir}/*")[1::]
    df = pd.concat(
        _struct_element_snapshot_query(p) for p in struct_paths
    ).reset_index()
    cols = ["path", "min", "max", "type", "mustSupport"]
    if must_support == True:
        df = df[df["mustSupport"] == True]
    df = df[cols]
    df["resourceType"] = df["path"].apply(lambda x: x.split(".")[0])
    if len(resource_types) > 0:
        df = df[df["resourceType"].isin(resource_types)]
    return df.reset_index(drop=True)
