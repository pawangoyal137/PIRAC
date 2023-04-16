import subprocess
import os
import re
import argparse
import numpy as np

from eval_pirac import benchmark_pirac
import utils

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for simplepir')
parser.add_argument('-ds','--dbSizes', nargs='+',
                     required=False, type=int, default=utils.LOG2_DB_SIZES,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int, default=utils.ELEM_SIZES,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the simplepir')
parser.add_argument('-off','--offline', action='store_true',
                     required=False, 
                     help='If the flag is passed, include the offline time')
parser.add_argument('-wp','--withPirac', choices=['re', 'pirac'],
                    required=False,
                    help='If passed "re", runs with reencryption. If passed with "pirac", run\
                        both rekeying and reencryption')

def run_SimplePIR(N, D, offline_include=False, output=False):
    if offline_include:
        test_name = "BenchmarkSimplePirOfflineIncludeSingle"
    else:
        test_name = "BenchmarkSimplePirSingle"
    process = subprocess.Popen(f"LOG_N={N} D={D} go test '-bench=^{test_name}$' -timeout 0 '-run=^$'", 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    throughput = None
    while True:
        line = process.stdout.readline()
        if "Avg SimplePIR tput, except for first run" in line:
            throughput = utils.extract_num(line)
        
        if output:
            print(line.rstrip())

        return_code = process.poll()
        if return_code is not None and output:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for line in process.stdout.readlines():
                print(line.strip())
            break
    
    return throughput

def benchmark_SimplePir(db_sizes, elem_sizes, offline_include=False, pirac_mode=None, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    throughputs = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            throughput = run_SimplePIR(db_size, elem_size, offline_include, output=output)
            offline_print = "(with offline time)" if offline_include else ""
            print(f"Throughput on SimplePIR {offline_print} with log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}Mb/s")
            throughputs.append(throughput)
    
    return throughputs

def pretty_print(throughputs, offline_include, pirac_mode):
    min_tput = np.min(throughputs)
    max_tput = np.max(throughputs)
    pp = f"Offline Mode = {offline_include}, Pirac Mode = {pirac_mode}\n"
    pp = pp + "Throughputs in the range {0:0.1f}-{1:0.1f}Mb/s".format(min_tput, max_tput)
    print(pp)

if __name__ == "__main__":
    args = parser.parse_args()
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    offline_include = args.offline
    output = args.output
    pirac_mode = args.withPirac

    os.chdir(utils.SimplePirPath)
    print(os.getcwd())

    throughputs_simplepir = benchmark_SimplePir(log2_db_sizes, elem_sizes, 
                        offline_include=offline_include, pirac_mode=pirac_mode, output=output)
    if pirac_mode is None:
        pretty_print(throughputs_simplepir, offline_include, pirac_mode)
    elif pirac_mode=="re":
        throughputs_re = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = False)
        throughputs_combined = utils.cal_tput_with_pirac(throughputs_simplepir, throughputs_re)
        pretty_print(throughputs_combined, offline_include, pirac_mode)
    elif pirac_mode=="pirac":
        throughputs_pirac = benchmark_pirac(log2_db_sizes, elem_sizes,  10, rekeying = True)
        throughputs_combined = utils.cal_tput_with_pirac(throughputs_simplepir, throughputs_pirac)
        pretty_print(throughputs_combined, offline_include, pirac_mode)
    else:
        raise Exception("Shouldn't reach here")
