# 导入matplotlib.pyplot
import matplotlib.pyplot as plt
# 导入pandas
import pandas as pd

# 读取CSV文件
data = pd.read_csv("书店图书销量和广告费用.csv")

# 通过 rcParams 参数将字体设置为微软雅黑
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 使用plt.scatter()函数
# 以data["ads_fee"]为x轴的值和data["sales"]为y轴的值
# 将颜色设置为绿色"green"，绘制散点图
plt.scatter(data["ads_fee"],data["sales"],color="green")

# 使用plt.xlabel()函数，将x轴标题设置为"广告费用"
plt.xlabel("广告费用")
# 使用plt.ylabel()函数，将y轴标题设置为"销量"
plt.ylabel("销量")

# 使用plt.show()函数显示图像
plt.show()