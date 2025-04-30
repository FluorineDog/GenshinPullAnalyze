# 简介
尝试分析原神抽卡新机制，明光捕获的概率模型

# 模型假设
基于 https://www.bilibili.com/video/BV13XBiYZErT/ 中提出的假设

并给小保底不歪 赋予额外的 `extra_prop` 概率


# 计算
```bash
python main.py
```
使用最大似然估计算法（MLE），基于现有的 workload，计算 `extra_pro` 的数值。

目前只支持了只包含 01 的歪与不歪的序列，还没有支持包含 012 的明光序列。
