# 导入matplotlib.pyplot
import matplotlib.pyplot as plt
# 导入pandas
import pandas as pd

# 读取CSV文件
data = pd.read_csv("书店每月销量数据.csv")
df = pd.read_csv("书店图书销量和广告费用.csv")

# 通过 rcParams 参数将字体设置为微软雅黑
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 使用plt.subplot()函数添加4个子图
# 子图有两行两列
# 选择序号为1子图
plt.subplot(2,2,1)
# 使用plt.plot()函数绘制折线图
plt.plot(data["month"],data["sum"])
# 使用plt.xticks()函数旋转x轴的刻度至90度
plt.xticks(rotation=90)

# 选择序号为2子图
plt.subplot(2,2,2)
# 使用plt.scatter()函数
# 以df["ads_fee"]为x轴的值和df["sales"]为y轴的值，绘制散点图
plt.scatter(df["ads_fee"],df["sales"])

# 选择序号为3的子图
plt.subplot(2,2,3)

# 选择序号为4子图
plt.subplot(2,2,4)

# 使用plt.tight_layout()函数来调整子图布局
plt.tight_layout()
# 使用plt.show()函数显示图像
plt.show()