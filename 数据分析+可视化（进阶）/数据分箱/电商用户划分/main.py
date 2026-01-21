
import pandas as pd

'''获取描绘R、F、M的数据'''

df = pd.read_csv("user_info.csv")

df["last_order_date"] = pd.to_datetime(df["last_order_date"])

# 获取描绘R的数据
from datetime import datetime

endTime = datetime(2019,4,1)
# 计算时间间隔
df["time_gap"] = endTime - df["last_order_date"]
# 将天数提取出来
df["time_gap"] = df["time_gap"].dt.days

'''依次划分R、F、M'''
# 1. 划分R
# 使用qcut()函数，将"time_gap"的数据分箱
# 均分为5组，区间标记命名为5-1
df["R"] = pd.qcut(df["time_gap"],q=5,labels=[5,4,3,2,1])

# 2. 划分F
# 使用qcut()函数，将"order_count"的数据分箱
# 均分为5组，区间标记命名为1-5
df["F"] = pd.qcut(df["order_count"],q=5,labels=[1,2,3,4,5])

# 3. 划分M
# 使用qcut()函数，将"total_amount"的数据分箱
# 均分为5组，区间标记命名为1-5
df["M"] = pd.qcut(df["total_amount"],q=5,labels=[1,2,3,4,5])

'''对用户标记分层结果'''
# 1. 简化分值
# 定义一个函数rfmTrans，如果参数x>3，就返回1；否则，就返回0
def rfmTrans(x):
    if x>3:
        return 1
    else:
        return 0

# 对R、F、M这三列数据，分别使用apply()函数
# 将函数名rfmTrans作为参数传入，并分别重新赋值给R、F、M这三列
df["R"] = df["R"].apply(rfmTrans)
df["F"] = df["F"].apply(rfmTrans)
df["M"] = df["M"].apply(rfmTrans)

# 2. 获取数值标签
# 用astype()函数将R、F、M这三列转化为字符串格式
# 再用"+"把字符串拼接在一起，组成一个新的列"mark"
df["mark"] = df["R"].astype(str)+df["F"].astype(str)+df["M"].astype(str)

# 3. 标记用户层级
# 定义一个函数rfmType，将数据标签，转化为对应的用户分层
def rfmType(x):
    if x=="111":
        return "高价值用户"
    elif x=="101":
        return "重点发展用户"
    elif x=="011":
        return "重点唤回用户"
    elif x=="001":
        return "重点潜力用户"
    elif x=="110":
        return "一般潜力用户"
    elif x=="100":
        return "一般发展用户"
    elif x=="010":
        return "一般维系用户"
    else:
        return "低价值用户"

# 对"mark""列，使用apply()函数
# 将函数名rfmType作为参数传入，并将结果赋值给df["customer_type"]
df["customer_type"] = df["mark"].apply(rfmType)

# 4. 可视化结果
# 4.1 计算每类用户总量
# 使用groupby()函数
# 将df["customer_type"]按照df["customer_type"]进行分组
# 然后使用count()函数进行聚合，赋值给变量df_type
df_type = df["customer_type"].groupby(df["customer_type"]).count()

# 获取每个层级的用户总数
total_user = df_type.values

# 4.2 计算每类用户占比
df_perc = df_type/51394

# 4.3数据可视化
# 导入matplotlib.pyplot，并使用"plt"作为该模块的简写
import matplotlib.pyplot as plt

# 通过给 plt.rcParams["font.sans-serif"] 赋值
# 字体设置
plt.rcParams["font.sans-serif"] = "Microsoft Yahei"

# 使用plt.bar()函数，绘制展示各层级用户总量的柱状图
# 以df_type.index为x轴的值df_type.values为y轴的值
# 将柱子的颜色设置为"skyblue"
plt.bar(df_type.index, df_type.values, color="skyblue")
# 使用plt.xlabel()函数，将x轴标题设置为"用户分层类别"
plt.xlabel("用户分层类别")
# 使用plt.ylabel()函数，将y轴标题设置为"各层级用户总数"
plt.ylabel("各层级用户总数")

# 使用plt.twinx()函数，添加另一个y轴
plt.twinx()

# 使用plt.plot()函数，绘制展示各层级用户占比的折线图
# 以df_perc.index为x轴的值，df_perc.values为y轴的值
# "o"作为标记点的样式，将折线颜色设置为"lightcoral"
plt.plot(df_perc.index, df_perc.values, marker="o", color="lightcoral")
# 使用plt.xlabel()函数，将x轴标题设置为"用户分层类别"
plt.xlabel("用户分层类别")
# 使用plt.ylabel()函数，将y轴标题设置为"各层级用户总数占比"
plt.ylabel("各层级用户总数占比")
plt.tight_layout()
plt.show()