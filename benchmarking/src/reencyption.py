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
    
    time_us_per_entry = [1000*time_ms[i]/db_sizes[i] for i in range(len(db_sizes))]
    plt.figure()
    plt.plot(np.log2(db_sizes), time_us_per_entry, "-o")
    plt.xlabel("Size of database in log")
    plt.ylabel("Time for rekeying/entry (in us)")
    plt.savefig("../images/rekeying.png")

    print("mean:{0:0.2f}, std:{1:0.3f}".format(np.mean(time_us_per_entry), np.std(time_us_per_entry)))

def benchmark_reencryption_dbsize(db_sizes, elem_size, num_iter=NUM_ITER):
    time_ms = []
    for size in db_sizes:
        t = []
        for _ in range(num_iter):
            t.append(c_lib.testReEncryption(size, elem_size))
        time_ms.append(np.mean(t))
    
    db_sizes_bits = [size * elem_size * 128 for size in db_sizes]
    db_sizes_mB = [i / BITS_IN_MB for i in db_sizes_bits]
    time_ms_per_mB = [time_ms[i]/db_sizes_mB[i] for i in range(len(time_ms))]
    plt.figure()
    plt.plot(np.log2(db_sizes), time_ms_per_mB, "-o")
    plt.xlabel("Size of database in log2")
    plt.ylabel("Time for reencryption/MB (in ms)")
    plt.savefig("../images/reencryption_dbsizes.png")

    print("mean:{0:0.2f}, std:{1:0.3f}".format(np.mean(time_ms_per_mB), np.std(time_ms_per_mB)))

def benchmark_reencryption_elem_size(db_size, elem_sizes, num_iter=NUM_ITER):
    time_ms = []
    for elem_size in elem_sizes:
        t = []
        for _ in range(num_iter):
            t.append(c_lib.testReEncryption(db_size, elem_size))
        time_ms.append(np.mean(t))
    
    db_sizes_bits = [db_size * elem_size * 128 for elem_size in elem_sizes]
    db_sizes_mB = [i / BITS_IN_MB for i in db_sizes_bits]
    time_ms_per_mB = [time_ms[i]/db_sizes_mB[i] for i in range(len(time_ms))]
    plt.figure()
    plt.plot(elem_sizes, time_ms_per_mB, "-o")
    plt.xlabel("Size of entry (in 128 bits)")
    plt.ylabel("Time for reencryption/MB (in ms)")
    plt.savefig("../images/reencryption_elemsize.png")

    print("mean:{0:0.2f}, std:{1:0.3f}".format(np.mean(time_ms_per_mB), np.std(time_ms_per_mB)))

if __name__ == "__main__":
    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "test.so"
    c_lib = ctypes.CDLL(libname)
    
    # Set return type as float
    c_lib.testReKeying.restype = ctypes.c_float
    c_lib.testReEncryption.restype = ctypes.c_float

    db_sizes = [1 << i for i in [10,12,14,16,18,20]]
    elem_sizes = [32, 64, 128, 256]

    benchmark_rekeying(db_sizes)
    benchmark_reencryption_dbsize(db_sizes, 128)
    benchmark_reencryption_elem_size(1<<20, elem_sizes)
    # throughputs = {}

    # for size in db_sizes:
    #     for elem_size in elem_sizes:
    #         time_rekeying = c_lib.testReKeying(size, elem_size)
    #         time_re_encryption = c_lib.testReEncryption(size, elem_size)

    #         db_size_bits = size * elem_size * 128
    #         bits_in_mb = 8 * 1000000
    #         db_size_mB = db_size_bits / bits_in_mb
    #         throughput = db_size_mB / ((time_rekeying+time_re_encryption) / 1000.0)
    #         throughputs[elem_size] = throughput
    #         print("Re-encryption for {}, {} in MB/s {}\n".format(size, elem_size, throughput))
    
    # print(throughputs)
