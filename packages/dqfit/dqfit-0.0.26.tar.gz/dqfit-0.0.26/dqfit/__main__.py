import sys
import json
import pandas as pd

from dqfit.services import Query
from dqfit.model import DQIModel

def main(srcdir: str, outdir:str, contexts: str, n=100) -> None:
    print(f"Loading Bundles from {srcdir}...")
    bundles = Query.bundles_query(srcdir, limit=n)
    
    for context_key in contexts.split("|"):
        model = DQIModel(context_key=context_key)
        result = model.fit(bundles=bundles)
        
        ####        
        index = dict(result[DQIModel.M].mean())
        with open(f"{outdir}/{context_key}-index.json", 'w') as f:
            json.dump(index, f)
        ###
        cohort_fhir_path = pd.concat(list(result['fhir_path']))
        cohort_fhir_path.to_csv(f"{outdir}/{context_key}-fhir_path.csv", index=False)
        ###
        path_summary = model.summarize(result=result)
        path_summary.to_csv(f"{outdir}/{context_key}-path_summary.csv", index=False)
        ###
        fig = model.visualize(result=result)
        fig.write_html(f"{outdir}/{context_key}-path_summary.html")
        ####
     
if __name__ == "__main__":
    try:
        main(
            srcdir=sys.argv[1], 
            outdir=sys.argv[2],
            contexts=sys.argv[3],
            n=int(sys.argv[4])
        )
    except Exception as e:
        print(e)
        print("To run the package: ")
        print("$ python -m dqfit SRCDIR OUTDIR 'CONTEXTS' N\n")
        print("For example:")
        print("$ python -m dqfit bundles/A . 'COLE|BCSE' N\n")
        print("SRCDIR: directory of FHIR Bundles as .json or .json.gz")
        print("OUTDIR: directory to store model output")
        print("CONTEXTS is pipe delimited string context keys in COLE|BCSE|PSA|ASFE; e.g. 'BCSE|COLE' ")
        print("N is number of bundles to include in model")
        


