import subprocess
import os
import json
import argparse
import numpy as np
import re
import math 

from eval_pirac import benchmark_pirac
from utils import cal_tput_with_pirac, SealPirPath

# declare the constants/ defaults for the experiments
LOG2_DB_SIZES = [14,16,18]

LOG2_ELEM_SIZES = [7, 9, 11, 13, 15]
ELEM_SIZES = [1<<i for i in LOG2_ELEM_SIZES]    # in bits

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for sealpir')
parser.add_argument('-ds','--dbSizes', nargs='+',
                     required=False, type=int, default=LOG2_DB_SIZES,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int, default=ELEM_SIZES,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the sealpir')
parser.add_argument('-wp','--withPirac', choices=['re', 'pirac'],
                    required=False,
                    help='If passed "re", runs with reencryption. If passed with "pirac", run\
                        both rekeying and reencryption')

def get_factor(itemsize, maxsize):
    factor = 1
    if itemsize <= maxsize:
        factor = 1
    else:
        factor = math.ceil(itemsize / maxsize)
    return factor

def run_SealPIR(N, D, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    maxsize = 24576 # 3072 bytes
    factor = get_factor(D, maxsize)
    elem_size = min(maxsize, D)
    process = subprocess.Popen(f'./main {N} {elem_size//8}', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    total_re = r"Main: PIRServer reply generation time.*:\s+([0-9]+)"
    exp_re = r"Server: Expansion time.*:\s+([0-9]+)"
    exp_us = 0
    if output:
        i = 0
        while True:
            output = process.stdout.readline()
            print(i, output.rstrip())
            i+=1
            try:
                total_us = int(re.search(total_re, output).group(1))*1000
            except:
                pass # invalid parsing

            try:
                exp_us += int(re.search(exp_re, output).group(1))
            except:
                pass # invalid parsing

            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    print(output.strip())
                break
    else:
        stdout, _ = process.communicate()
        total_us = int(re.search(total_re, stdout).group(1))*1000
        exp_us = sum([int(i) for i in re.findall(exp_re, stdout)])
    
    database_size_bytes = (1<<N)*(D//8)
    total_including_factor = (factor * (total_us-exp_us) + exp_us)
    print(f"Total server time: {total_us} us, Expansion Time: {exp_us} us, Total Time after factor = {total_including_factor} us")
    print(f"Factor = {factor}, elem size = {elem_size}")
    return database_size_bytes/total_including_factor

def benchmark_SealPir(db_sizes, elem_sizes, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    throughputs = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            throughput = run_SealPIR(db_size, elem_size, output)
            print(f"Throughput on SealPIR with log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}Mb/s")
            throughputs.append(throughput)
    
    return throughputs

def pretty_print(throughputs, pirac_mode):
    min_tput = np.min(throughputs)
    max_tput = np.max(throughputs)
    pp = f"Pirac Mode = {pirac_mode}\n"
    pp = pp + "Throughputs in the range {0:0.1f}-{1:0.1f}Mb/s".format(min_tput, max_tput)
    print(pp)

if __name__ == "__main__":
    args = parser.parse_args()
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    output = args.output
    pirac_mode = args.withPirac

    # for elem_size in elem_sizes:
    #     assert elem_size <= 10*1000*8, "Elem size should be <= 10KB" #current support is < 10KB

    os.chdir(SealPirPath)
    print(os.getcwd())
    
    throughputs_sealpir = benchmark_SealPir(log2_db_sizes, elem_sizes, output=output)

    if pirac_mode is None:
        pretty_print(throughputs_sealpir, pirac_mode)
    elif pirac_mode=="re":
        throughputs_re = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = False)
        throughputs_combined = cal_tput_with_pirac(throughputs_sealpir, throughputs_re)
        pretty_print(throughputs_combined, pirac_mode)
    elif pirac_mode=="pirac":
        throughputs_pirac = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = True)
        throughputs_combined = cal_tput_with_pirac(throughputs_sealpir, throughputs_pirac)
        pretty_print(throughputs_combined, pirac_mode)
    else:
        raise Exception("Shouldn't reach here")
