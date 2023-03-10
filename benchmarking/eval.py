from eval_pirac import benchmark_pirac
from eval_simplepir import benchmark_SimplePir
import matplotlib.pyplot as plt
import ctypes
import pathlib
import os

SimplePirPath = "../simplepir/pir"

if __name__ == "__main__":
    log2_db_sizes = [10,12,14,16,18,20]
    db_sizes = [1<<i for i in log2_db_sizes]

    log2_elem_sizes = [7, 9, 11, 13, 15]
    elem_sizes = [1<<i for i in log2_elem_sizes]

    owd = os.getcwd()

    os.chdir(SimplePirPath)
    simplepir = benchmark_SimplePir([12], elem_sizes)

    os.chdir(owd)
    pirac = benchmark_pirac([1<<12], [i//128 for i in elem_sizes], True, num_iter=5)

    plt.figure()
    plt.plot(log2_elem_sizes, simplepir, "r-o", label="SimplePIR")
    plt.plot(log2_elem_sizes, pirac, "b-o", label="PIRAC")
    plt.xlabel("log2 of Size of database entry (in bits)")
    plt.ylabel("Throughput (in Mb/s)")
    plt.legend()
    plt.savefig("images/comparision_elem_sizes.png")