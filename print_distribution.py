#python
import numpy as np
from guessed_mats import *
from entropy import calc_entropy
from collections import defaultdict
from parse_file import parse_file
 
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
 


def print_distribution(mats):
    # 定义状态空间
    n = mats[0].shape[0]
    states = [ "C" + str(i) for i in range(n)]
    
    # 初始化转移概率矩阵
    transition_matrix = np.zeros((n, n))
    transition_matrix = mats[0] + mats[1] + mats[2]

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

def print_all(extra_prop, required_state):
    mats = get_guessed_mats(extra_prop)
    print_distribution(mats)
    mats_2way = [mats[0], mats[1] + mats[2]]
    full_seqs = get_full_sequence(mats_2way, 15)
    res = calc_ratio_mat(full_seqs, 15, required_state)
    print_result(res)

def analyze_workload(workloads):
    # TODO how to fuck it ?
    final_res = defaultdict(float)   
    for seq, cnt in workloads:
        init = 0
        length = len(seq)
        for i in range(length):
            state = get_state(seq[init:i])
            if (state == 3):
                key = seq[init: i]  
                key = ''.join(map(str, key))
                key += '1'
                final_res[key] += cnt
                init = i + 1

        if init != length:
            key = seq[init: length]
            state = get_state(seq[init:length])
            key = ''.join(map(str, key))
            # print(key, "$")
            if state==3:
                key += '1'
            final_res[key] += cnt
    return final_res

def print_raw_workload(res):
    for key, value in res.items():
        print(f"{key} -> {value}")

def print_workload(workloads):
    aw = analyze_workload(workloads)
    res = calc_ratio_mat(aw, 15, 2)
    print_result(res)


if __name__ == '__main__':
    # extra_prop = 0
    # print_all(extra_prop, 2)
    # seq_bin = '00100100'
    # seq = [int(ch) for ch in seq_bin]
    # print(get_state(seq))

    workloads = parse_file('resources/workload2.txt')
    # print_workload(workloads)

    aw = analyze_workload(workloads)
    print_raw_workload(aw)