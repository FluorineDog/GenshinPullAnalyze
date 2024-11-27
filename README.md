# 简介
尝试分析原神抽卡新机制，明光捕获的概率模型

# 模型假设
基于 https://www.bilibili.com/video/BV13XBiYZErT/ 中提出的假设

并给 C2 状态增加额外的明光捕获概率 extra_prop

也就是 C2 状态有 `0.5` 的概率正常小保底，`extra_prop` 的概率触发明光机制，`0.5 - extra_prop` 的概率歪。

# 计算
```bash
python main.py
```
使用最大似然估计算法（MLE），基于现有的 workload，计算 `extra_pro` 的数值。

目前只支持了只包含 01 的歪与不歪的序列，还没有支持包含 012 的明光序列。

```bash
python print_distribution.py
```
打印 extra_prop 对应的概率矩阵，稳态分布，最终概率
