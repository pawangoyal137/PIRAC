import subprocess
import os
import re
import argparse
import numpy as np

from eval_pirac import benchmark_pirac

import utils
# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for paillier')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the simplepir')
parser.add_argument('-wp','--withPirac', choices=['re', 'pirac'],
                    required=False,
                    help='If passed "re", runs with reencryption. If passed with "pirac", run\
                        both rekeying and reencryption')

BITS = 2048

def run_Paillier(output=False):
    test_name = "BenchmarkPaillierDifPrimes"
    process = subprocess.Popen(f"go test '-bench=^{test_name}$' '-run=^$'", 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    throughput = None
    while True:
        line = process.stdout.readline()
        if "Average throughput for paillier" in line:
            throughput = utils.extract_num(line)
        
        if output:
            print(line.rstrip())

        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for line in process.stdout.readlines():
                print(line.strip())
            break
                
    print(f"Throughput of Paillier = {throughput} MB/s")
    return throughput

def pretty_print(throughput, pirac_mode):
    pp = f"Running Paillier, Pirac Mode = {pirac_mode}\n"
    pp = pp + "Throughput: {0:0.4f} MB/s".format(throughput)
    print(pp)

if __name__ == "__main__":
    args = parser.parse_args()
    output = args.output
    pirac_mode = args.withPirac

    os.chdir(utils.PaillierPath)

    throughput_paillier = run_Paillier(output=output)
    if pirac_mode is None:
        pretty_print(throughput_paillier, pirac_mode)
    elif pirac_mode=="re":
        throughputs_re = benchmark_pirac([16], [BITS],  10, rekeying = False)
        throughputs_combined = utils.cal_tput_with_pirac([throughput_paillier], throughputs_re)
        pretty_print(throughputs_combined[0], pirac_mode)
    elif pirac_mode=="pirac":
        throughputs_pirac = benchmark_pirac([16], [BITS],  10, rekeying = True)
        throughputs_combined = utils.cal_tput_with_pirac([throughput_paillier], throughputs_pirac)
        pretty_print(throughputs_combined[0], pirac_mode)
    else:
        raise Exception("Shouldn't reach here")
