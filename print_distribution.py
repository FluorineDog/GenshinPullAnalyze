#python
import numpy as np
from guessed_mats import *
from entropy import calc_entropy
 
def steady_state_distribution(P, tol=1e-10, max_iter=1000):
    n = P.shape[0]
    pi = np.ones(n) / n  # 初始分布为均匀分布
    for _ in range(max_iter):
        pi_new = pi @ P
        if np.allclose(pi, pi_new, atol=tol, rtol=0):
            break
        pi = pi_new
    return pi
 

    
    


def get_full_sequence(trans_mats, max_length):
    res = dict()
    init = np.array([0, 1, 0, 0])
    # generate all 0/1 string sequence with length 10
    for i in range(2**max_length):
        seq_bin = bin(i)[2:].zfill(max_length)
        seq = [int(ch) for ch in seq_bin]
        log_prop = calc_entropy(seq, trans_mats, init, 2)

        prop = np.exp(log_prop) if log_prop != -np.inf else 0
        res[seq_bin] = prop
    
    return res

def get_state(seq):
    state = 1 
    for i in seq:
        if state == 3:
            return None
            if i != 1:
                return None
            state = 1
            continue
        state += 1 - i * 2
        if state == -1:
            state = 0
    return state
             

def calc_ratio_mat(full_seqs, max_length, required_state):
    sum_prop = np.zeros((max_length, max_length))
    sum_prop_1 = np.zeros((max_length, max_length))

    # sort by entropy  
    for length in range(0, max_length):
        for seq_bin, prop in full_seqs.items():
            seq = [int(ch) for ch in seq_bin]
            if len(seq) <= length:
                continue
            is_hit = seq[length]
            subseq = seq[0:length]
            sum_of_seq = length - sum(subseq)
            state = get_state(subseq)
            if state != required_state:
                continue

            sum_prop[length, sum_of_seq] += prop
            sum_prop_1[length, sum_of_seq] += prop * is_hit
    ratio = sum_prop_1 / sum_prop
    return ratio

def print_result(res):
    # print this np.array in a table format
    print(f" ", end="\t")
    for i in range(res.shape[1]):
        print(f"{i}", end="\t")
    print()

    for j in range(res.shape[0]):
        print(f"{j}", end="\t")
        for i in range(res.shape[1]):
            print(f"{res[i, j]:.3f}", end="\t")
        print()
 


def print_distribution(extra_prop, required_state):
    # 定义状态空间
    states = ["C0", "C1", "C2", "C3"]
    
    # 初始化转移概率矩阵
    n = len(states)
    transition_matrix = np.zeros((n, n))


    mats = get_guessed_mats(extra_prop)
    transition_matrix = mats[0] + mats[1] + mats[2]
    mats_2way = [mats[0], mats[1] + mats[2]]

    # 可视化状态名和矩阵（可选）
    print("\n带有状态名的转移概率矩阵:")
    for i, state_i in enumerate(states):
        row = []
        for j, state_j in enumerate(states):
            row.append(f"{transition_matrix[i, j]:.2f} ({state_i} -> {state_j})")
        print("\t".join(row))
    
    # 打印转移概率矩阵
    print("转移概率矩阵:")
    print(transition_matrix)
    # 计算稳态分布
    pi = steady_state_distribution(transition_matrix)
    print("稳态分布:", pi)
    
    prop0 = float(np.sum(pi @ mats[0]))
    prop1 = float(np.sum(pi @ mats[1]))
    prop2 = float(np.sum(pi @ mats[2]))
    prop = 1 - np.sum(pi @ mats[0])
    print("最终不歪概率:", prop)
    print("最终概率:", [prop0, prop1, prop2])

    full_seqs = get_full_sequence(mats_2way, 15)
    res = calc_ratio_mat(full_seqs, 15, required_state)
    print_result(res)
   

if __name__ == '__main__':
    extra_prop = 0
    print_distribution(extra_prop, 2)
    # seq_bin = '00100100'
    # seq = [int(ch) for ch in seq_bin]
    # print(get_state(seq))