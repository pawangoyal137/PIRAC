
# declare the paths for the other PIR schemes
# relative to benchmarking folder
SimplePirPath = "../../simplepir/pir"
SpiralPirPath = "../../spiral"
SealPirPath = "../../SealPIR/bin"
PaillierPath = "../paillier"

# declare the constants/ defaults for the experiments
LOG2_DB_SIZE = 16
ELEM_SIZE = 1024

LOG2_DB_SIZES = [10,12,14,16,18]

LOG2_ELEM_SIZES = [7, 9, 11, 13, 15]
ELEM_SIZES = [1<<i for i in LOG2_ELEM_SIZES]    # in bits

def cal_tput_with_pirac(pir, pirac):
    return [1/(1/pir[i] + 1/pirac[i]) for i in range(len(pir))]