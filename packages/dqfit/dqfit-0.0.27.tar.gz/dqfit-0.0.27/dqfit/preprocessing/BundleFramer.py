import pandas as pd

def to_fhir_path(bundle: pd.Series) -> pd.DataFrame:

    def _frame_fhir_path_resource_type(resources: pd.DataFrame, resourceType="Condition") -> pd.DataFrame:
        """Doing this one resource type at a time so that can drop and melt"""
        if resourceType not in list(resources['resourceType']):
            return pd.DataFrame()
        
        def _get_fhir_path_name(key: str) -> str:
            if key in ['resourceType','id']:
                return key
            key = key.replace("Period", "[x]")
            key = key.replace("DateTime", "[x]")
            key = key.replace("valueQuantity", "value[x]")
            key = key.replace("valueRange", "value[x]")
            key = key.replace("valueCodeableConcept", "value[x]")
            key = key.replace("valueString", "value[x]")
            return f"{resourceType}.{key}"

        # rm not-relevant col
        df = (
            resources[resources["resourceType"] == resourceType]
            .dropna(axis=1, how="all")
            .reset_index(drop=True)
        )
        df.columns = [_get_fhir_path_name(key) for key in df.columns]  # to fhir_path-ey
        df = df.melt(id_vars=['resourceType',"id"]).rename(columns={"variable":"path"})

        return df

    entries = bundle['entry']
    resources = pd.DataFrame([e['resource'] for e in entries])
    resource_types = resources['resourceType'].unique()
    fhir_path = pd.concat([_frame_fhir_path_resource_type(resources, rt) for rt in resource_types]).reset_index(drop=True)
    fhir_path.insert(0, 'bundle_index', bundle['bundle_index'])
    return fhir_path