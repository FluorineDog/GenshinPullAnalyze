#python
import numpy as np
import math
from guessed_mats import get_guessed_mats

def calc_entropy(sequence, transfer_mats, init_prop_vec, scale_coef):
    prop_vec = init_prop_vec
    
    for index in sequence:
        mat = transfer_mats[index]
        prop_vec = prop_vec @ mat
        prop_vec *= scale_coef
    prop = np.log(np.sum(prop_vec))
    return prop

def main():
    # 定义状态空间
    states = ["C0", "C1", "C2", "C3"]
    all_trans_mats = get_guessed_mats(0.0)

    seq = [int(ch) for ch in "001001001001"]
    init = np.array([0, 1, 0, 0])
    delta_entropy = calc_entropy(seq, all_trans_mats, init, 2)

if __name__ == '__main__':
    main() 