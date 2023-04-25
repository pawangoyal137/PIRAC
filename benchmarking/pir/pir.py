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
                    choices=["simplepir", "spiralpir", "spiralstream", "spiralpack",
                    "spiralstreampack", "sealpir", "fastpir", "cwpir", "paillier"],
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
parser.add_argument('-pm','--piracModes', nargs='+', 
                    choices=["bl", 'mp', 'fs'],
                    required=False, type=str,
                    help='''Tell what modes to run. bl for baseline, mp for metadata private
                    and fs for forward safe''')
parser.add_argument('-arg','--arguments',
                    required=False, type=str,
                    help='Additional argument for the pir scheme')
parser.add_argument('-w','--writeFile',
                    required=False, type=str,
                    help='Tells where to write the results')
parser.add_argument('-ni','--numIter',
                     required=False, type=int,
                     default=5,
                     help='Number of interations to run experiments')

def cal_pir_tput(pir_name, log2_db_size, elem_size, add_arguments={}, output=False, num_iter=5):
    if pir_name=="simplepir":
        pir_tput =  cal_simplepir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name=="spiralpir":
        pir_tput = cal_spiralpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name=="spiralstream":
        pir_tput = cal_spiralpir_tput(log2_db_size, elem_size, output=output, stream=True, num_iter=num_iter, **add_arguments)
    elif pir_name=="spiralpack":
        pir_tput = cal_spiralpir_tput(log2_db_size, elem_size, output=output, pack=True, num_iter=num_iter,**add_arguments)
    elif pir_name=="spiralstreampack":
        pir_tput = cal_spiralpir_tput(log2_db_size, elem_size, output=output, pack=True, stream=True, num_iter=num_iter, **add_arguments)
    elif pir_name=="sealpir":
        pir_tput = cal_sealpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name=="fastpir":
        pir_tput = cal_fastpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name=="cwpir":
        pir_tput = cal_cwpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name=="paillier":
        pir_tput = cal_paillier_tput(log2_db_size, elem_size, output=output, **add_arguments)

    return pir_tput

def pretty_print(data, add_arguments):
    metadata_string = ""
    for k,v in add_arguments.items():
        metadata_string += f"{k} = {v}"
    if len(metadata_string)!=0:
        print(metadata_string) 
    df = utils.create_df(data)
    print(df)
    min_max_results = utils.find_max_min_pd_col(df, "tput")
    min_max_overhead = utils.find_max_min_pd_col(df, "overhead")
    for k,v in min_max_results.items():
        print("Range of {0:s}: {1:.2f}-{2:.2f}MB/s".format(k, v[0], v[1]))
    for k,v in min_max_overhead.items():
        print("Overhead of {0:s}: {1:.2f}-{2:.2f}MB/s".format(k, v[0], v[1]))

if __name__ == "__main__":
    args = parser.parse_args()
    pir_name = args.pir_name
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    output = args.output
    pirac_modes = args.piracModes
    write_file = args.writeFile
    add_arguments = json.loads(args.arguments) if args.arguments else {}
    num_iter = args.numIter

    for k,v in add_arguments.items():
        if v=="True":
            add_arguments[k]=True
        if v=="False":
            add_arguments[k]=False

    data = []
    for log2_db_size in log2_db_sizes:
        for elem_size in elem_sizes:
            pir_tput = cal_pir_tput(pir_name, log2_db_size, elem_size, add_arguments, output=output, num_iter=num_iter)            
            record = {"log2_db_size":log2_db_size, "elem_size":elem_size}
            for pm in pirac_modes:
                if pm=="bl":
                    record[f"{pir_name}_bl_tput"] = pir_tput
                elif pm=="mp":
                    re_tput = cal_pirac_tput(log2_db_size, elem_size,  num_iter, rekeying = False)
                    pir_re_tput = utils.cal_tput_with_pirac(pir_tput, re_tput)
                    record[f"{pir_name}_mp_tput"] = pir_re_tput
                    record[f"{pir_name}_mp_overhead"] = pir_tput/pir_re_tput
                elif pm=="fs":
                    pirac_tput = cal_pirac_tput(log2_db_size, elem_size,  num_iter, rekeying = True)
                    pir_pirac_tput = utils.cal_tput_with_pirac(pir_tput, pirac_tput)
                    record[f"{pir_name}_fs_tput"] = pir_pirac_tput
                    record[f"{pir_name}_fs_overhead"] = pir_tput/ pir_pirac_tput
                else:
                    raise Exception("Shouldn't reach here")

            data.append(record)
    
    pretty_print(data, add_arguments)
    if write_file is not None:
        with open(write_file, "w") as outfile:
            json.dump(data, outfile, separators=(",\n", ": "))