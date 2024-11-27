#python
import numpy as np
 
# 定义状态空间
states = ["C0", "C1", "C2", "C3"]
 
# 初始化转移概率矩阵
n = len(states)
transition_matrix = np.zeros((n, n))
 
# 填充转移概率矩阵
transition_matrix[0, 1] = 0.5
transition_matrix[1, 2] = 0.5
transition_matrix[2, 3] = 0.5
transition_matrix[3, 0] = 0.5

transition_matrix[3, 2] = 0.5
transition_matrix[2, 1] = 0.5
transition_matrix[1, 0] = 0.5
transition_matrix[0, 0] = 0.5
 
# 打印转移概率矩阵
print("转移概率矩阵:")
print(transition_matrix)
 
# 可视化状态名和矩阵（可选）
print("\n带有状态名的转移概率矩阵:")
for i, state_i in enumerate(states):
    row = []
    for j, state_j in enumerate(states):
        row.append(f"{transition_matrix[i, j]:.2f} ({state_i} -> {state_j})")
    print("\t".join(row))

def steady_state_distribution(P, tol=1e-10, max_iter=1000):
    n = P.shape[0]
    pi = np.ones(n) / n  # 初始分布为均匀分布
    for _ in range(max_iter):
        pi_new = pi @ P
        if np.allclose(pi, pi_new, atol=tol, rtol=0):
            break
        pi = pi_new
    return pi
 
# 计算稳态分布
pi = steady_state_distribution(transition_matrix)
print("稳态分布:", pi)

prop = (pi[0] + pi[1] + pi[2]) / 2.0 + pi[3]
print("最终概率:", prop)