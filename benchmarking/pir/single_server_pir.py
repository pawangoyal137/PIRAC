import argparse
import json
import numpy as np
import pandas as pd

from pirac import cal_pirac_tput
from cwpir import cal_cwpir_tput
from fastpir import cal_fastpir_tput
from paillier import cal_paillier_tput
from simplepir import cal_simplepir_tput
from spiralpir import cal_spiralpir_tput
from sealpir import cal_sealpir_tput

import utils

# define the parser for running the experiments
parser = argparse.ArgumentParser(
    description='Run benchmarking for a pir scheme')
parser.add_argument('-n', '--pir_name',
                    choices=["simplepir", "spiralpir", "spiralstream", "spiralpack",
                             "spiralstreampack", "sealpir", "fastpir", "cwpir", "paillier"],
                    required=True, type=str,
                    help='Name of the PIR scheme')
parser.add_argument('-ds', '--dbSizes', nargs='+',
                    required=False, type=int, default=utils.LOG2_DB_SIZES,
                    help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es', '--elemSizes', nargs='+',
                    required=False, type=int, default=utils.ELEM_SIZES,
                    help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-o', '--output', action='store_true',
                    required=False,
                    help='If the flag is passed, display the output of the pir')
parser.add_argument('-pm', '--piracModes', nargs='+',
                    choices=["bl", 'mp', 'fs'],
                    required=False, type=str, default=["bl"],
                    help='''Tell what modes to run. bl for baseline, mp for metadata private
                    and fs for forward safe''')
parser.add_argument('-arg', '--arguments',
                    required=False, type=str,
                    help='Additional argument for the pir scheme')
parser.add_argument('-w', '--writeFile',
                    required=False, type=str,
                    help='Tells where to write the results')
parser.add_argument('-ni', '--numIter',
                    required=False, type=int,
                    default=5,
                    help='Number of interations to run experiments')


def cal_pir_tput(pir_name, log2_db_size, elem_size, add_arguments={}, output=False, num_iter=5):
    if pir_name == "simplepir":
        return cal_simplepir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name == "spiralpir":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name == "spiralstream":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, stream=True, num_iter=num_iter, **add_arguments)
    elif pir_name == "spiralpack":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, pack=True, num_iter=num_iter, **add_arguments)
    elif pir_name == "spiralstreampack":
        return cal_spiralpir_tput(log2_db_size, elem_size, output=output, pack=True, stream=True, num_iter=num_iter, **add_arguments)
    elif pir_name == "sealpir":
        return cal_sealpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name == "fastpir":
        return cal_fastpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name == "cwpir":
        return cal_cwpir_tput(log2_db_size, elem_size, output=output, num_iter=num_iter, **add_arguments)
    elif pir_name == "paillier":
        return cal_paillier_tput(log2_db_size, elem_size, output=output, **add_arguments)


def pretty_print(data, add_arguments):
    metadata_string = ""
    for k, v in add_arguments.items():
        metadata_string += f"{k} = {v}"
    if len(metadata_string) != 0:
        print(metadata_string)
    df = utils.create_df(data)
    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
        print(df)
    min_max_results = utils.find_max_min_pd_col(df, "tput")
    min_max_overhead = utils.find_max_min_pd_col(df, "overhead")
    if min_max_results is not None:
        for k, v in min_max_results.items():
            units = "MB/s"
            if "std" in k:
                units = "%"
            print(
                "Range of {0:s}: {1:.2f}-{2:.2f}{3:s}".format(k, v[0], v[1], units))
    if min_max_overhead is not None:
        for k, v in min_max_overhead.items():
            print("Overhead of {0:s}: {1:.2f}-{2:.2f}".format(k, v[0], v[1]))


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

    for k, v in add_arguments.items():
        if v == "True":
            add_arguments[k] = True
        if v == "False":
            add_arguments[k] = False

    data = []
    for log2_db_size in log2_db_sizes:
        for elem_size in elem_sizes:
            pir_tput, pir_tput_std = cal_pir_tput(
                pir_name, log2_db_size, elem_size, add_arguments, output=output, num_iter=num_iter)
            # with open(f"results/data/single_server/{pir_name}.json") as f:
            #     df = pd.read_json(f)
            #     pir_tput = df.loc[(df['log2_db_size'] == log2_db_size) &
            #                         (df['elem_size'] == elem_size), f"{pir_name}_bl_tput"].values[0]
            #     pir_tput_std_pct = df.loc[(df['log2_db_size'] == log2_db_size) &
            #                         (df['elem_size'] == elem_size), f"{pir_name}_bl_tput_std_pct"].values[0]
            #     pir_tput_std = 0.01*pir_tput_std_pct*pir_tput
            record = {"log2_db_size": log2_db_size, "elem_size": elem_size}
            for pm in pirac_modes:
                if pm == "bl":
                    record[f"{pir_name}_bl_tput"] = pir_tput
                    record[f"{pir_name}_bl_tput_std_pct"] = 100 * \
                        pir_tput_std/pir_tput
                elif pm == "mp":
                    re_tput, re_tput_std = cal_pirac_tput(
                        log2_db_size, elem_size,  num_iter, key_refresh=False, output=output)
                    pir_re_tput = utils.cal_tput_with_pirac(pir_tput, re_tput)
                    record[f"{pir_name}_mp_tput"] = pir_re_tput
                    record[f"{pir_name}_mp_overhead"] = pir_tput/pir_re_tput
                    record[f"{pir_name}_mp_tput_std_pct"] = 100*pir_re_tput*(pir_tput_std/np.square(pir_tput) +
                                                                             re_tput_std/np.square(re_tput))
                elif pm == "fs":
                    pirac_tput, pirac_tput_std = cal_pirac_tput(
                        log2_db_size, elem_size,  num_iter, key_refresh=True, output=output)
                    pir_pirac_tput = utils.cal_tput_with_pirac(
                        pir_tput, pirac_tput)
                    record[f"{pir_name}_fs_tput"] = pir_pirac_tput
                    record[f"{pir_name}_fs_overhead"] = pir_tput / \
                        pir_pirac_tput
                    record[f"{pir_name}_fs_tput_std_pct"] = 100*pir_pirac_tput*(pir_tput_std/np.square(pir_tput) +
                                                                                pirac_tput_std/np.square(pirac_tput))
                else:
                    raise Exception("Shouldn't reach here")
            data.append(record)

    pretty_print(data, add_arguments)
    if write_file is not None:
        with open(write_file, "w") as outfile:
            json.dump(data, outfile, separators=(",\n", ": "))
