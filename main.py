from guessed_mats import get_guessed_mats
from entropy import calc_entropy
from parse_file import parse_file
import numpy as np

def sum_entropy(workloads, extra_prop):
    trans_mats = get_guessed_mats(extra_prop) 
    all_entropy = 0.0
    init_vec = np.array([0, 1.0, 0, 0])
    for arr, freq in workloads:
        entropy = calc_entropy(arr, trans_mats, init_vec, 2)
        all_entropy += entropy * freq
    return all_entropy

def ternary_search(f, left, right, epsilon=1e-9):
    """
    使用三分查找法在区间 [left, right] 内查找函数 f 的最大值点。
    
    参数:
    f -- 目标函数
    left -- 搜索区间的左边界
    right -- 搜索区间的右边界
    epsilon -- 精度阈值，用于决定搜索何时停止
    
    返回:
    mid -- 函数的最大值点
    """
    while right - left > epsilon:
        # 计算两个中间点
        one_third = (right - left) / 3
        mid1 = left + one_third
        mid2 = right - one_third
        
        # 比较两个中间点处的函数值
        if f(mid1) < f(mid2):
            left = mid1  # 如果 mid1 处的值小于 mid2 处的值，则峰值位于 mid1 右侧
        else:
            right = mid2  # 否则，峰值位于 mid2 左侧
            
    return (left + right) / 2

def main():
    workloads = parse_file('resources/log.txt')
    f = lambda extra_prop: sum_entropy(workloads, extra_prop)
    mle_prop = ternary_search(f, 0.0, 0.2)
    print("MLE of extra_prop =", mle_prop)

if __name__ == '__unittest__':
    main()