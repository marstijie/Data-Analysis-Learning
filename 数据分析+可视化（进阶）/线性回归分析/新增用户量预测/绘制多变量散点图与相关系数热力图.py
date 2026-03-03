import pandas as pd
df = pd.read_csv("multiple_to_new.csv")

import matplotlib.pyplot as plt

import seaborn as sns
# 绘制多变量散点图
sns.pairplot(df)

# 显示图像
plt.show()

# 计算相关性
df=df.drop("date", axis=1)
corr = df.corr()

# 绘制相关系数热力图
sns.heatmap(corr, cmap = "RdBu", square=True, annot = True)

# 显示图像
plt.show()