from eval_pirac import benchmark_pirac
from eval_simplepir import benchmark_SimplePir
from eval_spiralpir import benchmark_SpiralPir
import matplotlib.pyplot as plt
import ctypes
import pathlib
import os
import numpy as np

plt.style.use('seaborn')

SimplePirPath = "../simplepir/pir"
SpiralPirPath = "../../spiral"

DBSIZE = 16
if __name__ == "__main__":
    log2_db_sizes = [10,12,14,16,18,20]
    db_sizes = [1<<i for i in log2_db_sizes]

    log2_elem_sizes = [7, 9, 11, 13, 15]
    elem_sizes = [1<<i for i in log2_elem_sizes]

    owd = os.getcwd()

    os.chdir(SimplePirPath)
    simplepir = benchmark_SimplePir([DBSIZE], elem_sizes)

    os.chdir(owd)
    os.chdir(SpiralPirPath)
    spiralpir = benchmark_SpiralPir([DBSIZE], elem_sizes)

    os.chdir(owd)
    pirac = benchmark_pirac([1<<DBSIZE], [i//128 for i in elem_sizes], True, num_iter=5)

    plt.figure()
    plt.plot(log2_elem_sizes, np.log10(simplepir), "r-o", label="SimplePIR")
    plt.plot(log2_elem_sizes, np.log10(spiralpir), "g-o", label="SpiralPIR")
    plt.plot(log2_elem_sizes, np.log10(pirac), "b-o", label="PIRAC")
    plt.xlabel("log2 of Size of database entry (in bits)")
    plt.ylabel("Log10 of Throughput (in Mb/s)")
    plt.legend()
    plt.savefig("images/comparision_elem_sizes.png")