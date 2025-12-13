from zmd import *;

# 边界条件状态列表
boundary_states = [
    # 1. 大保底触发条件 (a=0, b=119)
    (0, 119, 0),   # 正常保底计数
    (0, 118, 20),   # 正常保底计数
    (0, 119, 50),  # 中等保底计数
    (0, 119, 65),  # 概率递增开始
    (0, 119, 79),  # 小保底触发点
    (0, 79, 79),  # 小保底触发点
    (0, 110, 79),  # 小保底触发点
    
    # 2. 赠送机制边界 (b=239)
    (1, 239, 0),   # a=0, 未满
    (4, 239, 0),   # a=4, 即将满
    (5, 239, 0),   # a=5, 会溢出重置
    (5, 239, 79),  # a=5, b=239, c=79 三重边界
    
    # 3. 小保底边界 (c=79)
    (0, 0, 79),    # 初始状态小保底
    (0, 77, 77),    # 初始状态小保底
    (2, 100, 79),  # 中间状态小保底
    (5, 0, 79),    # a=5时的小保底
    
    # 4. a溢出条件 (a=5)
    (5, 0, 0),     # 简单溢出条件
    (5, 100, 0),   # b不为0的溢出
    (5, 239, 50),  # 接近赠送的溢出
    
    # 5. 多重边界组合
    (0, 118, 79),  # 大保底前一次+小保底
    (0, 239, 79),  # 赠送前+小保底
    (5, 119, 79),  # a=5, 大保底b值, 小保底
    
    # 6. 正常状态参考
    (0, 0, 0),     # 初始状态
    (2, 150, 40),  # 一般中间状态
    (3, 50, 70),   # 高保底计数状态
]

indexing = 0
def print_transitions_for_state(a, b, c, transition_matrix):
    global indexing
    indexing = indexing + 1
    """打印指定状态的所有转移概率"""
    state_idx = encode_state(a, b, c)
    
    # 获取该状态的所有非零转移
    row = transition_matrix.getrow(state_idx)
    nonzero_cols = row.nonzero()[1]
    
    print(f"\n{indexing}: 状态 (a={a}, b={b}, c={c}):")
    print("-" * 50)
    
    if len(nonzero_cols) == 0:
        print("  无转移（可能状态编码错误）")
        return
    
    # 计算6星概率（用于参考）
    p_6star = get_6star_probability(c)
    print(f"  当前6星概率: {p_6star:.4f}")
    
    # 判断是否为特殊状态
    is_big_guarantee = (a == 0 and b == 119)
    is_gift_boundary = (b == 239)
    is_small_guarantee = (c == 79)
    is_a_overflow = (a == 5)
    
    special_flags = []
    if is_big_guarantee: special_flags.append("大保底触发")
    if is_gift_boundary: special_flags.append("赠送边界")
    if is_small_guarantee: special_flags.append("小保底")
    if is_a_overflow: special_flags.append("a可能溢出")
    
    if special_flags:
        print(f"  特殊标记: {', '.join(special_flags)}")
    
    # 显示转移
    print(f"  共有 {len(nonzero_cols)} 个转移:")
    
    total_prob = 0.0
    for col in nonzero_cols:
        a_new, b_new, c_new = decode_state(col)
        prob = transition_matrix[state_idx, col]
        total_prob += prob
        
        # 标记转移类型
        transfer_type = []
        if prob == 1.0:
            transfer_type.append("确定转移")
        elif prob > 0.5:
            transfer_type.append("高概率")
        elif prob < 0.1:
            transfer_type.append("低概率")
        
        # 判断是否是UP转移
        a_increased = (a_new == (a + 1) % 6 and a_new != a)
        is_up_transfer = a_increased and c_new == 0
        
        if is_up_transfer:
            transfer_type.append("获得UP")
        
        type_str = f" ({', '.join(transfer_type)})" if transfer_type else ""
        
        print(f"    → (a={a_new}, b={b_new}, c={c_new}) 概率: {prob:.6f}{type_str}")
    
    print(f"  概率总和: {total_prob:.10f}")
    print(f"  是否和为1: {'是' if abs(total_prob - 1.0) < 1e-10 else '否 (差异: ' + str(abs(total_prob - 1.0)) + ')'}")

def print_all_boundary_transitions(transition_matrix):
    """打印所有边界状态的转移"""
    print("=" * 70)
    print("边界条件转移概率检查")
    print("=" * 70)
    
    # 按照边界条件分组打印
    groups = [
        ("大保底触发条件 (a=0, b=119)", 
         [(a,b,c) for (a,b,c) in boundary_states if a==0 and b==119]),
        
        ("赠送机制边界 (b=239)", 
         [(a,b,c) for (a,b,c) in boundary_states if b==239]),
        
        ("小保底边界 (c=79)", 
         [(a,b,c) for (a,b,c) in boundary_states if c==79]),
        
        ("a溢出条件 (a=5)", 
         [(a,b,c) for (a,b,c) in boundary_states if a==5]),
        
        ("多重边界组合", 
         [(a,b,c) for (a,b,c) in boundary_states 
          if ((a==0 and b==118 and c==79) or 
              (a==0 and b==239 and c==79) or 
              (a==5 and b==119 and c==79))]),
        
        ("正常状态参考", 
         [(a,b,c) for (a,b,c) in boundary_states 
          if (a,b,c) in [(0,0,0), (2,150,40), (3,50,70)]]),
    ]
    
    for group_name, states in groups:
        if not states:
            continue
            
        print(f"\n{group_name}")
        print("=" * 50)
        
        for state in states:
            print_transitions_for_state(*state, transition_matrix)

def quick_verification(transition_matrix):
    """快速验证关键规则"""
    print("\n" + "=" * 70)
    print("关键规则快速验证")
    print("=" * 70)
    
    # 规则1: 大保底触发 (a=0, b=119) 必须只有1个转移，且转移到 (a=1, b=0, c=0)
    print("\n1. 大保底触发验证:")
    test_state = encode_state(0, 119, 50)
    row = transition_matrix.getrow(test_state)
    nonzero = row.nonzero()[1]
    
    if len(nonzero) == 1:
        target = decode_state(nonzero[0])
        prob = transition_matrix[test_state, nonzero[0]]
        if target == (1, 0, 0) and prob == 1.0:
            print("  ✓ 大保底规则正确: (0,119,50) → (1,0,0) 概率 1.0")
        else:
            print(f"  ✗ 大保底转移错误: 期望 (1,0,0) 概率 1.0，得到 {target} 概率 {prob}")
    else:
        print(f"  ✗ 大保底状态应有1个转移，实际有 {len(nonzero)} 个")
    
    # 规则2: 小保底 (c=79) 必须出6星
    print("\n2. 小保底验证:")
    test_state = encode_state(0, 0, 79)
    row = transition_matrix.getrow(test_state)
    nonzero = row.nonzero()[1]
    
    # 检查是否所有转移都重置了c（表示出了6星）
    all_reset_c = all(decode_state(col)[2] == 0 for col in nonzero)
    if all_reset_c:
        print("  ✓ 小保底正确: c=79时所有转移都重置c=0（必出6星）")
    else:
        print("  ✗ 小保底错误: 存在转移未重置c")
    
    # 规则3: a=5时获得UP会重置a=0且b=0
    print("\n3. a溢出重置验证:")
    # 我们需要找到a=5状态下的UP转移
    test_state = encode_state(5, 100, 0)
    row = transition_matrix.getrow(test_state)
    nonzero = row.nonzero()[1]
    
    up_transfers = []
    for col in nonzero:
        a_new, b_new, c_new = decode_state(col)
        # 判断是否是UP转移（a增加且c重置为0）
        if a_new == 0 and c_new == 0:  # a从5溢出到0
            prob = transition_matrix[test_state, col]
            up_transfers.append(((a_new, b_new, c_new), prob))
    
    if up_transfers:
        for target, prob in up_transfers:
            if target[1] == 0:  # b应该重置为0
                print(f"  ✓ a溢出重置正确: (5,100,0) → {target} 概率 {prob:.4f}，b重置为0")
            else:
                print(f"  ✗ a溢出重置错误: b未重置，b_new={target[1]}")
    else:
        print("  ? 未找到a=5的UP转移，需要进一步检查")
    
    # 规则4: 赠送机制 (b=239) 后a增加
    print("\n4. 赠送机制验证:")
    test_state = encode_state(4, 239, 0)  # a=4, b=239
    row = transition_matrix.getrow(test_state)
    nonzero = row.nonzero()[1]
    
    # 检查所有转移的a_new是否都>=5（因为a=4，赠送后至少为5）
    all_a_increased = all(decode_state(col)[0] >= 5 for col in nonzero)
    if all_a_increased:
        print("  ✓ 赠送机制正确: b=239时a增加")
    else:
        print("  ✗ 赠送机制错误: 存在转移a未增加")

def main():
    """主执行函数"""
    print("正在构建转移矩阵...")
    transition_matrix = build_transition_matrix_with_big_guarantee()
    print(f"转移矩阵构建完成！维度: {transition_matrix.shape}")
    
    # # 打印所有边界状态转移
    # print_all_boundary_transitions(transition_matrix)
    
    # # 快速验证
    # quick_verification(transition_matrix)
    
    # # 额外的状态检查
    # print("\n" + "=" * 70)
    # print("额外状态检查（可选）")
    # print("=" * 70)
    
    # 用户可以在这里添加想要检查的额外状态
    extra_states = boundary_states

    for state in extra_states:
        print_transitions_for_state(*state, transition_matrix)

# 执行主函数
if __name__ == "__main__":
    main()