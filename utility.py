import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime
import gc
import re

# File Reading

def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

def replacer(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string)
    return string

def col_header_val(df:pd.DataFrame, table_config):
    """
    replace whitespaces in the column and standardize column names
    """
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]','_',regex=True)
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns = list(map(lambda x: replacer(x,'_'), list(df.columns)))
    expected_col = list(map(lambda x: x.lower(),  table_config['columns']))
    expected_col.sort()
    df.columns =list(map(lambda x: x.lower(), list(df.columns)))
    df = df.reindex(sorted(df.columns), axis=1)

    if len(df.columns) == len(expected_col) and list(df.columns) == list(expected_col):
        print("Number of Columns and their length match")
        return 1
    
    else:
        print("Columns don't match")
        mismatched_columns = list(set(df.columns).difference(expected_col))
        print("Following File columns are not in the YAML file",mismatched_columns)
        missing_YAML = list(set(expected_col).difference(df.columns))
        print("Following YAML columns are not in the file uploaded",missing_YAML)
        logging.info(f'df.columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0
