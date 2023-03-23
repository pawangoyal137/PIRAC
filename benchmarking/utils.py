
def cal_tput_with_pirac(pir, pirac):
    return [1/(1/pir[i] + 1/pirac[i]) for i in range(len(pir))]