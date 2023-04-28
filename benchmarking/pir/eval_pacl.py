import pandas as pd
import json
import argparse
import math
import numpy as np

from pirac import cal_pirac_tput

import utils

SCHEMES = ["xor", "pir", "pir_keyword", "pir_pacl", "pir_keyword_baseline"]
JSON_PATH = '../../pacl/bench-pir/pir.json'

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for paillier')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the simplepir')

pd.set_option('display.max_columns', None)

def process_results(output=False):
    # Read the JSON file
    with open(JSON_PATH) as f:
        data = json.load(f)

    # Create a list of dictionaries with the desired columns
    processed_data = []
    pirac_tput_results = {}
    for d in data:
        db_size_bytes = d["db_size"]*d["item_size"]
        row = {
            'db_size': d['db_size'],
            'item_size': d['item_size']
        }
        for s in SCHEMES:
            row[f"{s}_us"] = np.mean(d[f'server_{s}_processing_ms'])
            row[f"{s}_tput"] = db_size_bytes/ (row[f"{s}_us"])
            row[f"{s}_tput_std_pct"] = 100*np.std(d[f'server_{s}_processing_ms'])/np.mean(d[f'server_{s}_processing_ms'])
        
        db_size_log2 = int(math.log2(d["db_size"]))
        item_size_bits = 8*d["item_size"]
        if (db_size_log2, item_size_bits) not in pirac_tput_results:
            pirac_tput_results[(db_size_log2, item_size_bits)] = cal_pirac_tput(18, 
                                                                    item_size_bits, 5, rekeying = True, output=True)
        pirac_tput, pirac_tput_std = pirac_tput_results[(db_size_log2, item_size_bits)]
        row["xor_pirac_tput"] = utils.cal_tput_with_pirac(row["xor_tput"], pirac_tput)
        row["pir_pirac_tput"] = utils.cal_tput_with_pirac(row["pir_tput"], pirac_tput)

        row["xor_pirac_tput_std_pct"] = (100*row["xor_pirac_tput"]*
                                (pirac_tput_std/np.square(pirac_tput)+0.01*row["xor_tput_std_pct"]/row["xor_tput"]))
        row["pir_pirac_tput_std_pct"] = (100*row["pir_pirac_tput"]*
                                (pirac_tput_std/np.square(pirac_tput)+0.01*row["pir_tput_std_pct"]/row["pir_tput"]))
        processed_data.append(row)
    
    with open("results/data/multi_server.json", "w") as f:
        json.dump(processed_data, f)

    if output:
        # Create a pandas DataFrame from the list of dictionaries
        df = pd.DataFrame(processed_data)

        # Set the db_size column as the index of the DataFrame
        df = df.set_index('db_size')

        # Sort the DataFrame by db_size and item_size in ascending order
        df = df.sort_values(['db_size', 'item_size'], ascending=[True, True])

        # Print the sorted DataFrame
        print(df)

    return processed_data

if __name__ == "__main__":
    args = parser.parse_args()
    output = args.output
    
    process_results(output)