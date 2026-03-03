# 导入Pandas模块
import pandas as pd
# 读取文件
df = pd.read_csv("wine.csv")

'''数据处理'''
# 将"proline"列的"low"，"medium"，"high"替换为0，1，2
df["proline"]=df["proline"].map({"low":0,"medium":1,"high":2})

# 删除"type"列，剩余的数据作为自变量x
x=df.drop(columns="type")

# 以二维结构读取"type"列，作为因变量y
y=df[["type"]]

# 导入sklearn.model_selection模块中的train_test_split函数
from sklearn.model_selection import train_test_split

# 划分训练集和测试集
# 设置测试集比例为0.2，随机参数为123
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=123)

'''模型预测'''
# 导入分类决策树模型DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
# 设置最大深度为2，随机参数为123，赋值给对象clf
clf=DecisionTreeClassifier(max_depth=2,random_state=123)

# 训练模型
clf.fit(x_train,y_train)

# 进行预测
y_pred=clf.predict(x_test)

from sklearn.metrics import accuracy_score

# 计算准确的样本数，并赋值给true_num
true_num=accuracy_score(y_pred,y_test,normalize=False)

# 计算预测错误的个数，赋值给false_num
false_num = len(y_pred)-true_num

'''可视化'''
# 导入可视化模块
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.sans-serif"]="Microsoft YaHei"

# 绘制柱状图
# X轴数据为["预测正确样本数","预测错误样本数"]，Y轴数据为[true_num,false_num]
# 设置color参数为["r","b"],设置width参数为0.5
plt.bar(["预测正确样本数","预测错误样本数"],[true_num,false_num],color=["r","b"],width=0.5)

# 设置标题为"预测情况"
plt.title("预测情况")

# 显示画布
plt.show()