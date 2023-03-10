import ctypes
import pathlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
NUM_ITER = 5
BITS_IN_MB = 8 * 1000000

# Load the shared library into ctypes
libname = "../acpir/src/test.so"
c_lib = ctypes.CDLL(libname)

# Set return type as float
c_lib.testReKeying.restype = ctypes.c_float
c_lib.testReEncryption.restype = ctypes.c_float

def benchmark_rekeying(db_sizes, figure=False, num_iter=NUM_ITER):
    entries_per_sec = []
    for db_size in db_sizes:
        t = []
        for _ in range(num_iter):
            t.append(c_lib.testReKeying(db_size))
        entry_per_sec = 1000*db_size/np.mean(t)
        entries_per_sec.append(entry_per_sec)
    
    if figure:
        plt.figure()
        plt.plot(np.log2(db_sizes), entries_per_sec, "-o")
        plt.xlabel("Size of database in log")
        plt.ylabel("Number of keys rekeyed per sec")
        plt.savefig("../images/rekeying.png")

    return entries_per_sec

def benchmark_pirac(db_sizes, elem_sizes, rekeying = False, figure=False, xvalues=None, xlabel=None, ylabel=None, figname=None, num_iter=NUM_ITER):
    """
    Take db sizes in abolsute values and elem_sizes as multiple of 128 bits
    """
    assert (len(db_sizes)==1 or len(elem_sizes)==1)

    throughputs = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            t = []
            for _ in range(num_iter):
                re_encrypt_time = c_lib.testReEncryption(db_size, elem_size)
                rekeying_time = c_lib.testReKeying(db_size) if rekeying else 0
                t.append(re_encrypt_time+rekeying_time)
            db_size_bits = db_size * elem_size * 128
            db_size_mB = db_size_bits / BITS_IN_MB
            throughput = 1000*db_size_mB/np.mean(t)
            print(f"Throughput on PIRAC with log2 dbsize = {np.log2(db_size)}, elem size = {128*elem_size} bits = {throughput}Mb/s")
            throughputs.append(throughput)   

    if figure:
        plt.figure()
        plt.plot(xvalues, throughputs, "-o")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(figname)

    return throughputs

if __name__ == "__main__":
    db_sizes = [1 << i for i in [10,12,14,16,18,20]]
    elem_sizes = [32, 64, 128, 256] # in 128 bits

    # rekeying benchmarking statistics
    benchmark_rekeying(db_sizes)

    # re-encryption benchmarking statistics
    benchmark_pirac(db_sizes, [128], False, True, np.log2(db_sizes), "Size of database in log2",
                     "Throughput for re-encryption in MB/s",  "../images/reencryption_dbsizes.png")
    benchmark_pirac([1<<12], elem_sizes, False, True, elem_sizes, "Size of entry (in 128 bits)",
                     "Throughput for re-encryption in MB/s", "../images/reencryption_elemsize.png")

    # complete benchmarking statistics
    benchmark_pirac(db_sizes, [128], True, True, np.log2(db_sizes), "Size of database in log2",
                    "Throughput for (rekeying+re-encryption) in MB/s",
                    "../images/pirac_dbsizes.png")
    benchmark_pirac([1<<12], elem_sizes, True, True, elem_sizes, "Size of entry (in 128 bits)",
                    "Throughput for (rekeying+re-encryption) in MB/s",
                    "../images/pirac_elemsize.png")
    
    # benchmark_pirac(db_sizes, [128], rekeying = True)