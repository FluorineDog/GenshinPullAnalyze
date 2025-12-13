import numpy as np
from scipy.sparse import lil_matrix

# 状态维度
A_DIM = 6   # 限定up数量 0-5
B_DIM = 240 # 赠送计数 0-239
C_DIM = 80  # 保底计数 0-79

# 总状态数
STATE_COUNT = A_DIM * B_DIM * C_DIM

def encode_state(a, b, c):
    """将三维状态编码为线性索引"""
    return a * (B_DIM * C_DIM) + b * C_DIM + c

def decode_state(idx):
    """将线性索引解码为三维状态"""
    a = idx // (B_DIM * C_DIM)
    temp = idx % (B_DIM * C_DIM)
    b = temp // C_DIM
    c = temp % C_DIM
    return a, b, c

def get_6star_probability(c):
    """根据保底计数c计算当前抽卡出6星的概率"""
    if c < 65:
        return 0.008  # 基础概率0.8%
    elif c < 79:
        # 65抽开始概率递增
        return 0.008 + (c - 64) * 0.05
    else:  # c == 79
        return 1.0  # 80抽保底

def next_state_after_pull(a, b, c, got_6star, got_up, force_big_guarantee=False):
    """
    计算一次抽卡后的状态转移
    
    参数:
        a: 当前限定up数量
        b: 当前赠送计数
        c: 当前保底计数
        got_6star: 是否抽到6星
        got_up: 是否抽到up角色
        force_big_guarantee: 是否触发大保底强制获得up
    """
    # 初始化新状态
    a_new, b_new, c_new = a, b, c
    
    # 处理大保底触发
    if force_big_guarantee:
        # 大保底：强制获得up，a增加，b重置，c重置
        a_new = (a + 1) % 6
        b_new = 0
        c_new = 0
        # 如果a超过5，重置为0（同时b已经为0）
        return a_new, b_new, c_new
    
    # 1. 更新b（赠送计数）
    b_new = (b + 1) % 240
    
    # 2. 检查是否触发赠送限定up（240抽赠送）
    if b == 239:  # 当前是第239抽，下一抽是第240抽
        a_new = a_new + 1
        if a_new == 0:  # 如果超过5个，重置为0
            b_new = 0  # 同时重置b
    
    # 3. 处理抽卡结果
    if got_6star:
        # 抽到6星，保底计数重置
        c_new = 0
        
        if got_up:
            # 抽到up角色
            a_new = a_new + 1
    else:
        # 没抽到6星，保底计数增加
        c_new = (c + 1) % 80

    if a_new > 5:
        a_new = 0
        b_new = 0
    
    return a_new, b_new, c_new

def build_transition_matrix_with_big_guarantee():
    """构建包含大保底规则的转移概率矩阵"""
    # 使用LIL格式便于逐步构建
    P = lil_matrix((STATE_COUNT, STATE_COUNT))
    
    # 遍历所有状态
    for a in range(A_DIM):
        for b in range(B_DIM):
            for c in range(C_DIM):
                current_state = encode_state(a, b, c)
                
                # 检查是否触发大保底条件
                force_big_guarantee = (a == 0 and b == 119)
                
                if force_big_guarantee:
                    # 触发大保底：强制获得up角色
                    a_new, b_new, c_new = next_state_after_pull(
                        a, b, c, False, False, force_big_guarantee=True
                    )
                    next_state = encode_state(a_new, b_new, c_new)
                    P[current_state, next_state] = 1.0
                else:
                    # 正常抽卡流程
                    p_6star = get_6star_probability(c)
                    
                    # 情况1: 没抽到6星 (概率: 1 - p_6star)
                    a1, b1, c1 = next_state_after_pull(a, b, c, False, False)
                    next_state1 = encode_state(a1, b1, c1)
                    P[current_state, next_state1] += 1 - p_6star
                    
                    # 情况2: 抽到6星但不是up (概率: p_6star * 0.5)
                    a2, b2, c2 = next_state_after_pull(a, b, c, True, False)
                    next_state2 = encode_state(a2, b2, c2)
                    P[current_state, next_state2] += p_6star * 0.5
                    
                    # 情况3: 抽到6星且是up (概率: p_6star * 0.5)
                    a3, b3, c3 = next_state_after_pull(a, b, c, True, True)
                    next_state3 = encode_state(a3, b3, c3)
                    P[current_state, next_state3] += p_6star * 0.5
    
    # 转换为CSR格式以提高计算效率
    return P.tocsr()
