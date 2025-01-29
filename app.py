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

def to_json(df, tgt_base_dir, ds_name, file_name):
    json_file_path = f"{tgt_base_dir}\\{ds_name}\\{file_name}"
    os.makedirs(f"{tgt_base_dir}\\{ds_name}", exist_ok=True)
    df.to_json(json_file_path,
               orient='records',
               lines=True)

def file_converter(ds_name, src_base_dir, tgt_base_dir):   
    schemas = json.load(open(f"{src_base_dir}/schemas.json"))
    files = glob.glob(f"{src_base_dir}\\{ds_name}\\part-*")
    print(files)

    for file in files:
        df = read_csv(file, schemas)
        file_name = re.split('[/\\\]', file)[-1]
        to_json(df,tgt_base_dir,ds_name, file_name)

def process_files(ds_names=None,
                  src_base_dir = "data\\retail_db",
                    tgt_base_dir = "data\\retail_db_json"):
    schemas = json.load(open(f"{src_base_dir}\\schemas.json"))
    if not ds_names:
        ds_names = schemas.keys()
    for ds_name in ds_names:
        print(f"Processing {ds_name}")
        file_converter(ds_name=ds_name,
                       src_base_dir=src_base_dir,
                       tgt_base_dir=tgt_base_dir)