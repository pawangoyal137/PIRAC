import argparse
import os
import json
import sys

from pirac import cal_pirac_tput
from cwpir import cal_cwpir_tput
from fastpir import cal_fastpir_tput
from paillier import cal_paillier_tput
from simplepir import cal_simplepir_tput
from spiralpir import cal_spiralpir_tput
from sealpir import cal_sealpir_tput

import utils

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for a pir scheme')
parser.add_argument('-n','--pir_name',
                     required=True, type=str,
                     help='Name of the PIR scheme')
parser.add_argument('-ds','--dbSizes', nargs='+',
                     required=False, type=int, default=utils.LOG2_DB_SIZES,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int, default=utils.ELEM_SIZES,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the pir')
parser.add_argument('-wp','--withPirac', choices=['re', 'pirac'],
                    required=False,
                    help='If passed "re", runs with reencryption. If passed with "pirac", run\
                        both rekeying and reencryption')
parser.add_argument('-arg','--arguments',
                     required=False, type=str,
                     help='Additional argument for the pir scheme')
parser.add_argument('-w','--writeFile',
                     required=False, type=str,
                     help='Tells where to write the results')

def pretty_print(data, add_arguments, pirac_mode):
    metadata_string = ""
    for k,v in add_arguments.items():
        metadata_string += f"{k} = {v}"
    if len(metadata_string)==0:
        print(f"Pirac Mode = {pirac_mode}") 
    else:
        print(metadata_string+ f" Pirac Mode = {pirac_mode}")
    df = utils.create_df(data)
    print(df)
    max_tput, min_tput = utils.find_max_min_pd_col(df, "tput")
    print("Throughputs in the range {0:.2f}-{1:.2f}MB/s".format(min_tput, max_tput))

def change_dir(pir_name):
    if pir_name=="simplepir":
        os.chdir(utils.SimplePirPath)
    elif pir_name=="sealpir":
        os.chdir(utils.SealPirPath)
    elif pir_name=="fastpir":
        os.chdir(utils.FastPirPath) 
    elif pir_name=="cwpir":
        os.chdir(utils.CWPirPath)
    elif pir_name=="paillier":
        os.chdir(utils.PaillierPath)
    elif "spiral" in pir_name:  # for "spiralpir", "spiralstream", "spiralpack", "spiralstreampack"
        os.chdir(utils.SpiralPirPath)

def cal_pir_tput(log2_db_size, elem_size, add_arguments, output):
    if pir_name=="simplepir":
        return cal_simplepir_tput(log2_db_size, elem_size, output=output, **add_arguments)
    elif pir_name=="spiralpir":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, **add_arguments)
    elif pir_name=="spiralstream":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, stream=True, **add_arguments)
    elif pir_name=="spiralpack":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, pack=True, **add_arguments)
    elif pir_name=="spiralstreampack":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, pack=True, stream=True, **add_arguments)
    elif pir_name=="sealpir":
        return cal_sealpir_tput(log2_db_size, elem_size, output=output, **add_arguments)
    elif pir_name=="fastpir":
        return cal_fastpir_tput(log2_db_size, elem_size, output=output, **add_arguments)
    elif pir_name=="cwpir":
        return cal_cwpir_tput(log2_db_size, elem_size, output=output, **add_arguments)
    elif pir_name=="paillier":
        return cal_paillier_tput(log2_db_size, elem_size, output=output, **add_arguments)

if __name__ == "__main__":
    args = parser.parse_args()
    pir_name = args.pir_name
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    output = args.output
    pirac_mode = args.withPirac
    write_file = args.writeFile
    add_arguments = json.loads(args.arguments) if args.arguments else {}

    for k,v in add_arguments.items():
        if v=="True":
            add_arguments[k]=True
        if v=="False":
            add_arguments[k]=False

    cwd = os.getcwd()
    change_dir(pir_name)

    data = []
    for log2_db_size in log2_db_sizes:
        for elem_size in elem_sizes:
            pir_tput = cal_pir_tput(log2_db_size, elem_size, add_arguments, output=output)            
            record = {"log2_db_size":log2_db_size, "elem_size":elem_size}
            if pirac_mode is None:
                record[f"{pir_name}_tput"] = pir_tput
            elif pirac_mode=="re":
                re_tput = cal_pirac_tput(log2_db_size, elem_size,  10, rekeying = False)
                pir_re_tput = utils.cal_tput_with_pirac(pir_tput, re_tput)
                record[f"{pir_name}_re_tput"] = pir_re_tput
            elif pirac_mode=="pirac":
                pirac_tput = cal_pirac_tput(log2_db_size, elem_size,  10, rekeying = True)
                pir_pirac_tput = utils.cal_tput_with_pirac(pir_tput, pirac_tput)
                record[f"{pir_name}_pirac_tput"] = pir_pirac_tput
            else:
                raise Exception("Shouldn't reach here")

            data.append(record)
    
    pretty_print(data, add_arguments, pirac_mode)
    os.chdir(cwd)
    if write_file is not None:
        with open(write_file, "w") as outfile:
            json.dump(data, outfile, separators=(",\n", ": "))