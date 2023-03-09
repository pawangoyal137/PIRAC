import ctypes
import pathlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
NUM_ITER = 5
BITS_IN_MB = 8 * 1000000

def benchmark_rekeying(db_sizes, num_iter=NUM_ITER):
    time_ms = []
    for size in db_sizes:
        t = []
        for _ in range(num_iter):
            t.append(c_lib.testReKeying(size))
        time_ms.append(np.mean(t))
    
    entries_per_sec = [1000*db_sizes[i]/time_ms[i] for i in range(len(db_sizes))]
    plt.figure()
    plt.plot(np.log2(db_sizes), entries_per_sec, "-o")
    plt.xlabel("Size of database in log")
    plt.ylabel("Number of keys rekeyed per sec")
    plt.savefig("../images/rekeying.png")

    print("mean:{0:0.2f}, std:{1:0.3f}".format(np.mean(entries_per_sec), np.std(entries_per_sec)))

def benchmark_pirac(db_sizes, elem_sizes, xvalues, xlabel, ylabel, figname, rekeying = False, num_iter=NUM_ITER):
    assert (len(db_sizes)==1 or len(elem_sizes)==1)

    time_ms = []
    for db_size in db_sizes:
        for elem_size in elem_sizes:
            t = []
            for _ in range(num_iter):
                re_encrypt_time = c_lib.testReEncryption(db_size, elem_size)
                rekeying_time = c_lib.testReKeying(db_size) if rekeying else 0
                t.append(re_encrypt_time+rekeying_time)
            time_ms.append(np.mean(t))
    
    
    db_sizes_bits = [db_size * elem_size * 128 for elem_size in elem_sizes for db_size in db_sizes]
    db_sizes_mB = [i / BITS_IN_MB for i in db_sizes_bits]
    time_ms_per_mB = [time_ms[i]/db_sizes_mB[i] for i in range(len(time_ms))]
    throughput = [1000/i for i in time_ms_per_mB]

    plt.figure()
    plt.plot(xvalues, throughput, "-o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(figname)

    print("mean:{0:0.2f}, std:{1:0.3f}".format(np.mean(throughput), np.std(throughput)))

if __name__ == "__main__":
    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "test.so"
    c_lib = ctypes.CDLL(libname)
    
    # Set return type as float
    c_lib.testReKeying.restype = ctypes.c_float
    c_lib.testReEncryption.restype = ctypes.c_float

    db_sizes = [1 << i for i in [10,12,14,16,18,20]]
    elem_sizes = [32, 64, 128, 256] # in 128 bits

    # print individual benchmarking statistics
    benchmark_rekeying(db_sizes)
    benchmark_pirac(db_sizes, [128], np.log2(db_sizes), "Size of database in log2",
                     "Throughput for re-encryption in MB/s",  "../images/reencryption_dbsizes.png")
    benchmark_pirac([1<<20], elem_sizes, elem_sizes, "Size of entry (in 128 bits)",
                     "Throughput for re-encryption in MB/s", "../images/reencryption_elemsize.png")

    # complete benchmarking statistics
    benchmark_pirac(db_sizes, [128], np.log2(db_sizes), "Size of database in log2",
                    "Throughput for (rekeying+re-encryption) in MB/s",
                    "../images/pirac_dbsizes.png", rekeying=True)
    benchmark_pirac([1<<20], elem_sizes, elem_sizes, "Size of entry (in 128 bits)",
                    "Throughput for (rekeying+re-encryption) in MB/s",
                    "../images/pirac_elemsize.png", rekeying=True)