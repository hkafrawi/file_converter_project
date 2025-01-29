import os
import json
import glob
import pandas as pd
import re

def get_column_names(schemas,ds_name,sorting_key="column_position"):
    column_details = schemas[ds_name]
    columns = sorted(column_details, key= lambda col:col[sorting_key] )

    return [col["column_name"] for col in columns]

def read_csv(file, schemas):
    file_details = re.split('[/\\\]', file)
    ds_name = file_details[-2]
    file_name = file_details[-1]
    columns = get_column_names(schemas, ds_name)
    df = pd.read_csv(file,names=columns)

    return df
