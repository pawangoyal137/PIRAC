import subprocess
import os
import argparse
import numpy as np
import math

import utils

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for spiralpir')
parser.add_argument('-ds','--dbSize',
                     required=True, type=int, 
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSize',
                     required=True, type=int,
                     help='Element size (in bits) to run experiment on.')
parser.add_argument('-hs','--hammingSize', type=int,
                     required=True, 
                     help='Hamming Size')
parser.add_argument('-kw','--keyWordLength', type=int,
                     required=True, 
                     help='Size of the keywords in bit length')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the spiralpir')

def run_CWPIR(db_size, elem_size, kw, h, output=False):
    """
    Take db sizes in log 2 and elem_sizes in bits
    """
    num_entries = (1<<db_size)
    elem_size_bytes = elem_size//8
    process = subprocess.Popen(f'./main -n {num_entries} -s {elem_size_bytes} -x {kw} -h {h} -d 13 -e 1 -t 1', 
                            shell=True,
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    statistics = {}
    correct_response = False   
    i = 0
    while True:
        line = process.stdout.readline()
        if output:
            print(i, line.rstrip())
            i+=1
            
        if "Number of Keywords" in line:
            assert utils.extract_num(line)==num_entries
        elif "Keyword Max Bitlength" in line:
            assert utils.extract_num(line)==kw
        elif "Max Item Hex Length" in line:
            assert utils.extract_num(line)==elem_size_bytes*2
        elif "Hamming Weight" in line:
            assert utils.extract_num(line)==h
        elif "Correct Response!" in line:
            correct_response = True
        elif "Response Cipher Count" in line:
            statistics["num_output_ciphers"] = utils.extract_num(line)
        elif "Total Server" in line:
            statistics["total_ms"] = utils.extract_num(line)

        

        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for line in process.stdout.readlines():
                print(line.strip())
            break
    
    assert correct_response
    assert statistics is not None

    elem_size_mb =  ((2**13) * statistics["num_output_ciphers"] * 20 / 8000000)
    db_size_mb = num_entries * elem_size_mb
    throughput = 1000*db_size_mb/statistics["total_ms"]

    print(f"Throughput on CWPIR  with kw = {kw}, Hamming weight = {h} \n\
         log2 dbsize = {db_size}, elem size = {elem_size} bits = {throughput}MB/s")
    return 

# def pretty_print(throughputs, stream, pack, pirac_mode):
#     min_tput = np.min(throughputs)
#     max_tput = np.max(throughputs)
#     pp = f"Streaming = {stream}, Packing = {pack}, Pirac Mode = {pirac_mode}\n"
#     pp = pp + "Throughputs in the range {0:0.1f}-{1:0.1f}Mb/s".format(min_tput, max_tput)
#     print(pp)

if __name__ == "__main__":
    args = parser.parse_args()
    log2_db_size = args.dbSize
    elem_size = args.elemSize
    h = args.hammingSize
    kw = args.keyWordLength
    output = args.output

    os.chdir(utils.CWPIR)
    print(os.getcwd())

    run_CWPIR(log2_db_size, elem_size, kw, h, output=output)
