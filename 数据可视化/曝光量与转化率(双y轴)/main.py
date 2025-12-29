# 导入matplotlib.pyplot
import matplotlib.pyplot as plt

# 导入pandas
import pandas as pd

# 读取CSV文件
data = pd.read_csv("每月曝光量和转化率.csv")

# 将字体设置为微软雅黑
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 使用plt.bar()函数
# 以data["month"]为x轴的值，data["exposure"]为y轴的值
# 将柱子的颜色设置为"skyblue"，"PV"作为图例，绘制曝光量的柱状图
plt.bar(data["month"],data["exposure"],color="skyblue",label="PV")
# 使用plt.xlabel()函数，设置x轴标题
plt.xlabel("月份")
# 使用plt.ylabel()函数，设置y轴标题
plt.ylabel("曝光量")

# 将图例显示在左上角
plt.legend(loc="upper left")

# 添加另一个y轴
plt.twinx()

# 使用plt.plot()函数
# 以data["month"]为x轴的值，data["CVR"]为y轴的值
#  "o"作为标记点的样式，"CVR"作为图例，绘制转化率的折线图
plt.plot(data["month"],data["CVR"],marker="o",label="CVR")
# 使用plt.ylabel()函数，将y轴标题设置为"转化率"
plt.ylabel("转化率")
# 使用plt.legend()函数显示图例
plt.legend()

# 使用plt.show()函数显示图像
plt.show()