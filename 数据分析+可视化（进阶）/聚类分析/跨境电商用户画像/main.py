import pandas as pd

'''读取数据集并获取特征变量'''
df = pd.read_csv("new_user_info.csv")

# 获取特征变量x
x = df[["time_gap", "order_count", "total_amount"]]

'''数据归一化'''
# 导入sklearn.preprocessing模块中的StandardScaler类
from sklearn.preprocessing import StandardScaler

# 创建一个StandardScaler对象
scaler = StandardScaler()

# 对x进行归一化
x_scale = scaler.fit_transform(x)

'''进行KMeans算法的聚类运算'''
# 导入sklearn.cluster模块中的KMeans模型
from sklearn.cluster import KMeans

# 使用KMeans()初始化模型
# 设置参数n_clusters=3, random_state=1
model = KMeans(n_clusters=3, random_state=1)

model.fit(x_scale)

# 获取每个样本所属的簇
labels = model.labels_

'''可视化结果'''

import matplotlib.pyplot as plt

# 从mpl_toolkits.mplot3d中导入Axes3D类
from mpl_toolkits.mplot3d import Axes3D

# 字体设置
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

fig = plt.figure(figsize=(12, 8))

# 创建3D坐标轴对象
ax = fig.add_subplot(projection="3d")

color = ["dodgerblue", "seagreen", "lightcoral"]


for i in range(0, 3):

    d = x[labels == i]

    ax.scatter(d["time_gap"], d["order_count"], d["total_amount"], color=color[i], label=f"用户群体{i}")

# 设置x轴标题为"R"
ax.set_xlabel("R")
# 设置y轴标题为"F"
ax.set_ylabel("F")
# 设置z轴标题为"M"
ax.set_zlabel("M")

plt.legend()

plt.show()