# 导入matplotlib.pyplot
import matplotlib.pyplot as plt
# 导入pandas
import pandas as pd

# 读取CSV文件
data = pd.read_csv("书店每月销量数据百分比.csv")

# 将字体设置为微软雅黑
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 使用plot.bar()函数
# 根据data变量，以"month"为x轴，["一楼","二楼","三楼"]为y轴
# 绘制百分比堆积柱状图
data.plot.bar("month",["一楼","二楼","三楼"],stacked=True)

# 使用plt.show()函数显示图像
plt.show()