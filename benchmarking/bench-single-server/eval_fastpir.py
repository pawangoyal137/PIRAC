import subprocess
import os
import json
import argparse
import numpy as np
import re

from eval_pirac import benchmark_pirac

import utils

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for fastpir')
parser.add_argument('-ds','--dbSizes', nargs='+',
                     required=False, type=int, default=utils.LOG2_DB_SIZES,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int, default=utils.ELEM_SIZES,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the sealpir')
parser.add_argument('-wp','--withPirac', choices=['re', 'pirac'],
                    required=False,
                    help='If passed "re", runs with reencryption. If passed with "pirac", run\
                        both rekeying and reencryption')


def run_FastPIR(N, D, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    maxsize = 72960 # 9120 bytes
    factor = utils.get_factor(D, maxsize)
    elem_size = min(maxsize, D)
    process = subprocess.Popen(f'bin/fastpir -n {1<<N} -s {elem_size//8}', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    correct_result = False
    while True:
        line = process.stdout.readline()
        if "Response generation time" in line:
            total_us = utils.extract_num(line)
        if "PIR result correct!" in line:
            correct_result = True

        if output:
            print(line.rstrip())

        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for line in process.stdout.readlines():
                print(line.strip())
            break

    assert correct_result
    database_size_bytes = (1<<N)*(D//8)
    total_including_factor = factor * total_us

    if output:
        print(f"Factor = {factor}, elem size = {elem_size}")
        print(f"Total server time: {total_us} us, Total Time after factor = {total_including_factor} us")
    return database_size_bytes/total_including_factor

def benchmark_FastPir(db_sizes, elem_sizes, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    throughputs = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            throughput = run_FastPIR(db_size, elem_size, output)
            print(f"Throughput on FastPIR with log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}Mb/s")
            throughputs.append(throughput)
    
    return throughputs

def pretty_print(throughputs, pirac_mode):
    min_tput = np.min(throughputs)
    max_tput = np.max(throughputs)
    pp = f"Pirac Mode = {pirac_mode}\n"
    pp = pp + "Throughputs in the range {0:0.2f}-{1:0.2f}MB/s".format(min_tput, max_tput)
    print(pp)

if __name__ == "__main__":
    args = parser.parse_args()
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    output = args.output
    pirac_mode = args.withPirac

    os.chdir(utils.FastPirPath)
    print(os.getcwd())
    
    throughputs_fastpir = benchmark_FastPir(log2_db_sizes, elem_sizes, output=output)

    if pirac_mode is None:
        pretty_print(throughputs_fastpir, pirac_mode)
    elif pirac_mode=="re":
        throughputs_re = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = False)
        throughputs_combined = utils.cal_tput_with_pirac(throughputs_fastpir, throughputs_re)
        pretty_print(throughputs_combined, pirac_mode)
    elif pirac_mode=="pirac":
        throughputs_pirac = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = True)
        throughputs_combined = utils.cal_tput_with_pirac(throughputs_fastpir, throughputs_pirac)
        pretty_print(throughputs_combined, pirac_mode)
    else:
        raise Exception("Shouldn't reach here")
