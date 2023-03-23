import ctypes
import pathlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import argparse

# np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
NUM_ITER = 5
BITS_IN_MB = 8 * 1000000

# Load the shared library into ctypes
libname = "../acpir/src/test.so"
c_lib = ctypes.CDLL(libname)

# Set return type as float
c_lib.testReKeying.restype = ctypes.c_float
c_lib.testReEncryption.restype = ctypes.c_float

# declare the constants/ defaults for the experiments
LOG2_DB_SIZE = 16
ELEM_SIZE = 1024

LOG2_DB_SIZES = [10,12,14,16,18]

LOG2_ELEM_SIZES = [7, 9, 11, 13, 15]
ELEM_SIZES = [1<<i for i in LOG2_ELEM_SIZES]    # in bits

# define the parser for running the experiments
parser = argparse.ArgumentParser(description='Run benchmarking for PIRAC')
parser.add_argument('-b','--benchType', choices=['rk', 're', 'pir'],    # re-keying, re-encryption and pirac
                     required=True, type=str,
                     help='Tells script what aspect to benchmark')
parser.add_argument('-e','--expType', choices=['ds', 'es'],
                     required=True, type=str,
                     help='Tells file if to run db_size or elem_size experiments')
parser.add_argument('-ds','--dbSizes', nargs='+',
                     required=False, type=int,
                     help='Log 2 Database sizes to run experiment on.')
parser.add_argument('-es','--elemSizes', nargs='+',
                     required=False, type=int,
                     help='Element sizes (in bits) to run experiment on.')
parser.add_argument('-n','--numIter',
                     required=False, type=int,
                     default=NUM_ITER,
                     help='Number of interations to run experiments')

def benchmark_rekeying(num_iter):
    time_array = []
    db_size = 1 << LOG2_DB_SIZE
    for _ in range(num_iter):
        time_array.append(c_lib.testReKeying(db_size))
    # KEY_SIZE = 128 #bits
    # ms_per_MB_array = [i*BITS_IN_MB/(db_size*KEY_SIZE) for i in time_array]
    records_per_sec_array = [db_size*1000/i for i in time_array]
    
    return records_per_sec_array

def benchmark_pirac(log2_db_sizes, elem_sizes,  num_iter, rekeying = False, throughput=True):
    """
    Take db sizes in log base 2 and elem_sizes in bits
    """

    throughputs = []
    records_per_sec_array = []
    db_sizes = [1<<i for i in log2_db_sizes]
    elem_sizes_128 = [i//128 for i in elem_sizes]
    for db_size in db_sizes:
        for elem_size in elem_sizes_128:
            t = []
            for _ in range(num_iter):
                re_encrypt_time = c_lib.testReEncryption(db_size, elem_size)
                rekeying_time = c_lib.testReKeying(db_size) if rekeying else 0
                t.append(re_encrypt_time+rekeying_time)
            if throughput:
                db_size_bits = db_size * elem_size * 128
                db_size_mB = db_size_bits / BITS_IN_MB
                throughput = 1000*db_size_mB/np.mean(t)
                print(f"Throughput on PIRAC with log2 dbsize = {np.log2(db_size)}, elem size = {128*elem_size} bits = {throughput}Mb/s")
                throughputs.append(throughput)  
            else:
                records_per_sec = 1000*db_size/np.mean(t) 
                print(f"Throughput on PIRAC with log2 dbsize = {np.log2(db_size)}, elem size = {128*elem_size} bits = {records_per_sec}records/s")
                records_per_sec_array.append(records_per_sec)

    return throughputs if throughput else records_per_sec_array


if __name__ == "__main__":
    args = parser.parse_args()
    bench_type = args.benchType
    exp_type = args.expType
    log2_db_sizes = args.dbSizes
    elem_sizes = args.elemSizes
    num_iter = args.numIter

    if exp_type=="ds":
        log2_db_sizes = LOG2_DB_SIZES if log2_db_sizes is None else log2_db_sizes
        elem_sizes = [ELEM_SIZE] if elem_sizes is None else elem_sizes
    elif exp_type=="es":
        log2_db_sizes = [LOG2_DB_SIZE] if log2_db_sizes is None else log2_db_sizes
        elem_sizes = ELEM_SIZES if elem_sizes is None else elem_sizes
    else:
        raise Exception("Shouldn't reach here")
    
    if bench_type == "rk":
        entries_per_sec = benchmark_rekeying(num_iter)
        print("Throughput:{0:0.0f} keys/sec +- {1:0.0f}".format(np.mean(entries_per_sec), np.std(entries_per_sec)))
    elif bench_type == "re":
        throughputs = benchmark_pirac(log2_db_sizes, elem_sizes,  num_iter, throughput=False)
        print(throughputs)
    elif bench_type == "pir":
        throughputs = benchmark_pirac(log2_db_sizes, elem_sizes,  num_iter, True, throughput=False)
        print(throughputs)