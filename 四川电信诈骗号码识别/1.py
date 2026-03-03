# -*- coding: utf-8 -*-
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 混淆矩阵数据（基于表4-1 Light-GBM指标反向推导，精准匹配准确率0.93、精确率0.88、召回率0.94）
# 真实标签：正常（行0）、欺诈（行1）；预测标签：正常（列0）、欺诈（列1）
cm = np.array([[847, 118], [28, 437]])
labels = ['正常', '欺诈']

# 绘制热力图
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
            xticklabels=labels, yticklabels=labels,
            annot_kws={'size': 14}, cbar_kws={'label': '样本数量'})

# 添加标题和标签
plt.title('Light-GBM模型混淆矩阵（准确率：0.93）', fontsize=16)
plt.xlabel('预测标签', fontsize=14)
plt.ylabel('真实标签', fontsize=14)
plt.tight_layout()
plt.savefig('lightgbm_cm.png', dpi=300, bbox_inches='tight')
plt.show()