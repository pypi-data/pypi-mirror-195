import pandas as pd
from tqdm import tqdm
from typing import List
import plotly.express as px
tqdm.pandas()

from dqfit.categories import Complete, Conformant, Plausible, Timely
from dqfit.preprocessing import BundleFramer
from dqfit.services import Query, ContextManager

class DQIModel:

    M = ['Conformant','Complete','Plausible']

    def __init__(self, context_key: str) -> None:
        self.context_key = context_key

    def score_fhir_path(self, bundle) -> pd.DataFrame:
        """
            Takes in bundle, converts to fhir_path DataFrame
        
            Returns a `fhir_path` DataFrame, that has been scored
            by one of each dimension in : Conformant, Complete, Plausible
        """
        fhir_path = BundleFramer.to_fhir_path(bundle)
        fhir_path["Context"] = self.context_key
        fhir_path = Conformant.fit(fhir_path, self.context_key) 
        fhir_path = fhir_path[fhir_path['Conformant']==1]
        fhir_path = Complete.fit(fhir_path, self.context_key)
        fhir_path = Plausible.fit(fhir_path, self.context_key)
        # fhir_path = Timely.score(fhir_path, context_key)
        return fhir_path.reset_index(drop=True)
    
    def agg_fhir_path(self, fhir_path: pd.DataFrame) -> pd.DataFrame:
        """Takes in scored fhir_path """
        fhir_path_agg = fhir_path.groupby(["resourceType", "path"]).agg(
                document_count=("bundle_index", "nunique"),
                term_count=("path", "count"),
                Conformant=("Conformant", "mean"), # mean of means
                Complete=("Complete", "mean"),
                Plausible=("Plausible", "mean"),
                Conformant_std=("Conformant", "std"), 
                Complete_std=("Complete", "std"),
                Plausible_std=("Plausible", "std"),
                # Timely=("Timely", "max"),
            ).reset_index()
        context_expects = pd.DataFrame(dict(path = ContextManager.load_context(self.context_key)['path']))
        context_expects['resourceType'] = context_expects['path'].apply(lambda x: x.split('.')[0])
        fhir_path_agg = fhir_path_agg.merge(context_expects, how='outer').fillna(0)
        fhir_path_agg.insert(0, 'bundle_index', fhir_path['bundle_index'].unique()[0]) # gross
        return fhir_path_agg
    
    def fit(self, bundles: pd.DataFrame) -> pd.DataFrame:
        context = ContextManager.load_context(self.context_key)
        print(f"{self.context_key} m={len(context['path'])} | n={len(bundles)}")
        result = bundles.copy()
        result['Context'] = self.context_key
        result['fhir_path'] = result.progress_apply(self.score_fhir_path, axis=1)
        # result['fhir_path'] = result.apply(self.score_fhir_path, axis=1)
        result['_fhir_path_shape'] = result['fhir_path'].apply(lambda x: x.shape)
        result['_fhir_path_agg'] = result['fhir_path'].apply(self.agg_fhir_path)
        result['_fhir_path_agg_shape'] = result['_fhir_path_agg'].apply(lambda x: x.shape)
        for dim in self.M:
            # n of 1 score
            # are these two actually the same thing?
            result[dim] = result['_fhir_path_agg'].apply(lambda x: x[dim].mean()) # mean of means?
            # result[dim] = result['fhir_path_agg'].apply(lambda x: x[dim].sum())
        result['Score'] = result[self.M].sum(axis=1)
        result = result.drop(columns=['entry','type'])
        result.insert(3, 'entry',"DROP") # no need to cache or propogate
        return result
    
    def summarize(self, result: pd.DataFrame, sort_by_dims=True) -> pd.DataFrame:
        cohort_fhir_path_agg = pd.concat(list(result["_fhir_path_agg"]))
        # I should be able to do this from result['fhir_path']?
        # ^ actually, if we're doing the context expects thing...

        df = cohort_fhir_path_agg.groupby(["path"]).agg(
            document_total=("bundle_index", "nunique"),
            term_total=("term_count", "sum"),
            Conformant=("Conformant", "mean"),  # mean of means
            Complete=("Complete", "mean"),
            Plausible=("Plausible", "mean"),
            Conformant_std=("Conformant", "std"),
            Complete_std=("Complete", "std"),
            Plausible_std=("Plausible", "std"),
        ).reset_index()
        if sort_by_dims:
            df = df.sort_values(self.M, ascending=False).reset_index(drop=True)
        # print(df.shape)
        df.insert(0, 'Context', self.context_key)
        df.insert(1, 'resourceType', df['path'].apply(lambda x: x.split(".")[0]))
        return df

    def visualize(self, result: pd.DataFrame):
        df = self.summarize(result)[["path", *self.M]]
        df = df.melt(id_vars=['path'])
        df['resourceType'] = df['path'].apply(lambda x: x.split('.')[0])
        return px.scatter(
            df,
            y="path",
            x="value",
            color="resourceType",
            facet_col="variable",
            # hover_data = ['document_total','term_total'],
            title=f"n={len(result)} | context:{self.context_key} | {dict(result[self.M].mean())}",
        )

    def filter_by_path(self, result, path):
        df = pd.concat(list(result["fhir_path"]))
        df = df[df["path"] == path].sort_values(self.M, ascending=False)
        return df.reset_index(drop=True)

    def filter_by_resourceType(self, result, resourceType: str):
        df = pd.concat(list(result["fhir_path"]))
        df = df[df["resourceType"] == resourceType].sort_values(self.M, ascending=False)
        return df.reset_index(drop=True)    
    
    def visualize_comparison(self, results: List[pd.DataFrame]):
        dfs = []
        for idx, result in enumerate(results):
            df = self.summarize(result)
            df.insert(0, 'cohort_index', idx)
            dfs.append(df)
        summaries = pd.concat(dfs)
        summaries
        return px.scatter(
            summaries.melt(id_vars=['resourceType','path','cohort_index','Context'], value_vars=self.M),
            y="path",
            x="value",
            color="resourceType",
            facet_col="variable",
            facet_row="cohort_index",
            height=800,
            title=f"Cohort Comparison | context:{summaries['Context'].unique()}",
        )