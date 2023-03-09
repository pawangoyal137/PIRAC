import ctypes
import pathlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('tkagg')

def benchmark_rekeying(db_sizes):
    time_ms = []
    for size in db_sizes:
        t = c_lib.testReKeying(size)
        time_ms.append(t)
    
    time_us_per_entry = [1000*time_ms[i]/db_sizes[i] for i in range(len(db_sizes))]
    plt.figure()
    plt.plot(np.log2(db_sizes), time_us_per_entry, "-o")
    plt.xlabel("Size of database in log")
    plt.ylabel("Time for rekeying/entry (in us)")
    plt.savefig("../images/rekeying.png")

    print("mean:{.2f}, std:{.2f}".format(np.mean(time_us_per_entry), np.std(time_us_per_entry)))


if __name__ == "__main__":
    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "test.so"
    c_lib = ctypes.CDLL(libname)
    
    # Set return type as float
    c_lib.testReKeying.restype = ctypes.c_float
    c_lib.testReEncryption.restype = ctypes.c_float

    db_sizes = [1 << i for i in [10,15,20,25]]
    # db_sizes = [1 << i for i in [20]]
    elem_sizes = [32, 64, 128, 256]

    benchmark_rekeying(db_sizes)
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