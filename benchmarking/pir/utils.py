import os
import re
import math
import pandas as pd
from functools import reduce

# declare the paths for the other PIR schemes
# relative to benchmarking folder
FastPirPath = "../../FastPIR"
SimplePirPath = "../../SimplePIR/pir"
SpiralPirPath = "../../spiral"
SealPirPath = "../../SealPIR/bin"
PaillierPath = "../paillier"
CWPirPath = "../../constant-weight-pir/src/build"

# declare the constants/ defaults for the experiments
LOG2_DB_SIZE = 20
ELEM_SIZE = 1024

LOG2_DB_SIZES = [16,18,20]

LOG2_ELEM_SIZES = [7, 9, 11, 13, 15]
ELEM_SIZES = [1<<i for i in LOG2_ELEM_SIZES]    # in bits

def cal_tput_with_pirac(pir, pirac, batch=1):
    return batch/(batch/pir + 1/pirac)

def cal_tput_for_comb(pir, pir_with_pirac, batch=1):
    return batch/((batch-1)/pir + 1/pir_with_pirac)

def extract_num(s):
    """
    Return the numbers in s
    """
    pattern = r"[-+]?\d*\.\d+|\d+"  # Regular expression for matching integers and floats
    match = re.search(pattern, s)
    if match:
        return float(match.group())
    else:
        return None

def get_factor(itemsize, maxsize):
    factor = 1
    if itemsize <= maxsize:
        factor = 1
    else:
        factor = math.ceil(itemsize / maxsize)
    return factor

def create_df(data):
    # Create a pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Sort the DataFrame by db_size and item_size in ascending order
    df = df.sort_values(['log2_db_size', 'elem_size'], ascending=[True, True])

    return df

def find_max_min_pd_col(df, col_name_like):
    # Filter columns that contain "tput"
    cols = [col for col in df.columns if col_name_like in col]
    if len(cols)==0:
        return None

    # Calculate min and max values for each column
    result = df[cols].agg(['min', 'max'])

    # Convert resulting DataFrame into a dictionary
    output_dict = {}
    for col in cols:
        output_dict[col] = [result.loc['min', col], result.loc['max', col]]

    return output_dict

def concatenate_jsons(directory, verbose=False):
    """
    Create a combined json merged on log2_db_size and elem_size
    """
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"): 
            filenames.append(os.path.join(directory, filename))
            continue

    dfs = []
    for fname in filenames:
        dfs.append(pd.read_json(fname))

    df_merged = reduce(lambda  left,right: pd.merge(left,right,
                on=['log2_db_size', "elem_size"], how='outer'), dfs).fillna('void')
    df_merged = df_merged.sort_values(by=['log2_db_size', 'elem_size'])

    if verbose:
        print(df_merged)
    
    return df_merged