import ctypes
import pathlib

if __name__ == "__main__":
    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "test.so"
    c_lib = ctypes.CDLL(libname)
    
    # Set return type as float
    c_lib.testReKeying.restype = ctypes.c_float
    c_lib.testReEncryption.restype = ctypes.c_float

    # db_sizes = [1 << i for i in [10,15,20,25]]
    db_sizes = [1 << i for i in [20]]
    elem_sizes = [32, 64, 128, 256]

    throughputs = {}

    for size in db_sizes:
        for elem_size in elem_sizes:
            time_rekeying = c_lib.testReKeying(size, elem_size)
            time_reencryptioin = c_lib.testReEncryption(size, elem_size)

            db_size_bits = size * elem_size * 128
            bits_in_mb = 8 * 1000000
            db_size_mB = db_size_bits / bits_in_mb
            throughput = db_size_mB / ((time_rekeying+time_reencryptioin) / 1000.0)
            throughputs[elem_size] = throughput
            print("Re-encryption for {}, {} in MB/s {}\n".format(size, elem_size, throughput))
    
    print(throughputs)