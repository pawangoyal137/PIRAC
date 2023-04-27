import ctypes
import pathlib
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import json

import utils
# np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
NUM_ITER = 5
BITS_IN_MB = 8 * 1000000

# Load the shared library into ctypes
libname = "../acpir/src/test.so"
c_lib = ctypes.CDLL(libname)

# Set return type as float
c_lib.testReKeying.restype = ctypes.c_float
c_lib.testReEncryption.restype = ctypes.c_float

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for PIRAC')
parser.add_argument('-b','--benchType', choices=['rk', 're', 'pirac'],    # re-keying, re-encryption and pirac
                     required=True, type=str,
                     help='Tells script what aspect to benchmark')
parser.add_argument('-ds','--dbSizes', nargs='+', default=utils.LOG2_DB_SIZES,
                     required=False, type=int,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+', default=utils.ELEM_SIZES,
                     required=False, type=int,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-n','--numIter',
                     required=False, type=int,
                     default=NUM_ITER,
                     help='Number of interations to run experiments')
parser.add_argument('-t','--throughput', action='store_true',
                     required=False, default=False,
                     help='If the flag is passed, return benchmark as MB/s \
                         instead of records per sec')
parser.add_argument('-w','--writeFile',
                     required=False, type=str,
                     help='Tells where to write the results')
parser.add_argument('-o','--output', action='store_true',
                     required=False, 
                     help='If the flag is passed, display the output of the pirac')

def cal_rekeying_tput(num_iter=5):
    time_array = []
    db_size = 1 << utils.LOG2_DB_SIZE
    for _ in range(num_iter):
        time_array.append(c_lib.testReKeying(db_size))
    records_per_sec_array = [db_size*1000/i for i in time_array]
    
    return records_per_sec_array

def cal_pirac_tput(log2_db_size, elem_size,  num_iter=5, rekeying = False, throughput=True, output=False):
    """
    Take db sizes in log base 2 and elem_sizes in bits
    """
    db_size = 1<<log2_db_size
    elem_size_128 = elem_size//128

    t = []
    for _ in range(num_iter):
        re_encrypt_time = c_lib.testReEncryption(db_size, elem_size_128)
        rekeying_time = c_lib.testReKeying(db_size) if rekeying else 0
        t.append(re_encrypt_time+rekeying_time)
    if throughput:
        db_size_bits = db_size * elem_size_128 * 128
        db_size_mB = db_size_bits / BITS_IN_MB
        throughput = 1000*db_size_mB/np.mean(t)
        tput_std = throughput*np.std(t)/np.mean(t)
        if output:
            print(f"Throughput on PIRAC with log2 dbsize = {np.log2(db_size)}, elem size = {128*elem_size_128} bits = {throughput}MB/s")
        return throughput, tput_std
    else:
        records_per_sec = 1000*db_size/np.mean(t) 
        records_per_sec_std = records_per_sec*np.std(t)/np.mean(t)
        if output:
            print(f"Throughput on PIRAC with log2 dbsize = {np.log2(db_size)}, elem size = {128*elem_size_128} bits = {records_per_sec}records/s")
        return records_per_sec, records_per_sec_std

def pretty_print(data, bench_type):
    print(f"Running Experiments for = {bench_type}")
    df = utils.create_df(data)
    print(df)
    max_tput, min_tput = utils.find_max_min_pd_col(df, "tput")
    print("Throughputs in the range {0:.2f}-{1:.2f}MB/s".format(min_tput, max_tput))

if __name__ == "__main__":
    args = parser.parse_args()
    bench_type = args.benchType
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    num_iter = args.numIter
    throughput = args.throughput
    write_file = args.writeFile
    output = args.output

    data = []
    for log2_db_size in log2_db_sizes:
        for elem_size in elem_sizes:
            if bench_type == "rk":
                entries_per_sec = cal_rekeying_tput(num_iter)
                record = {"log2_db_size":log2_db_size, "elem_size":elem_size, f"{bench_type}_tput":np.mean(entries_per_sec)}
            elif bench_type == "re":
                re_tput = cal_pirac_tput(log2_db_size, elem_size,  num_iter, throughput=throughput)
                record = {"log2_db_size":log2_db_size, "elem_size":elem_size, f"{bench_type}_tput":re_tput}
            elif bench_type == "pirac":
                pirac_tput = cal_pirac_tput(log2_db_size, elem_size,  num_iter, True, throughput=throughput)
                record = {"log2_db_size":log2_db_size, "elem_size":elem_size, f"{bench_type}_tput":pirac_tput}
            
            data.append(record)
    
    pretty_print(data, bench_type)
    if write_file is not None:
        with open(write_file, "w") as outfile:
            json.dump(data, outfile, separators=(",\n", ": "))