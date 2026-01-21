# 导入matplotlib.pyplot
import matplotlib.pyplot as plt
# 导入pandas
import pandas as pd

# 读取CSV文件
data = pd.read_csv("书店每月销量数据.csv")

# 通过 rcParams 参数将字体设置为微软雅黑
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 使用plt.plot()函数
# 以data["month"]为x轴的值和data["sum"]为y轴的值，将颜色设置为"orange"，"o"作为标记点的样式
# "每月总销量"作为图例，绘制折线图
plt.plot(data["month"],data["sum"],color="orange",marker="o",label="每月总销量")

# 使用plt.xlabel()函数，将x轴标题设置为"月份"
plt.xlabel("月份")
# 使用plt.ylabel()函数，将y轴标题设置为"销量"
plt.ylabel("销量")
# 使用plt.title()函数，将图表标题设置为"2019年8月至2020年7月书店每月销量走势"
plt.title("2019年8月至2020年7月书店每月销量走势")

# 使用plt.legend()函数显示图例
plt.legend()
# 使用plt.show()函数显示图像
plt.show()

# 使用plt.bar()函数
# 以data["month"]为x轴的值和data["sum"]为y轴的值，绘制柱状图
plt.bar(data["month"],data["sum"])

# 使用plt.show()函数显示图像
plt.show()

# 绘制簇型柱状图
data.plot.bar("month",["first_floor","second_floor","third_floor"])

# 使用plt.show()函数显示图像
plt.show()