# 从sklearn.datasets中导入数据集函数
from sklearn.datasets import load_diabetes

# 使用load_diabetes()获取数据集，赋值到boston
boston = load_diabetes()

# 获取数据集的特征部分，赋值到x
x = boston.data

# 获取数据集的目标部分，赋值到y
y = boston.target

# 导入sklearn.model_selection模块中的train_test_split函数
from sklearn.model_selection import train_test_split

# 使用train_test_split()函数划分训练集和测试集
# 设置测试集比例为0.2，随机参数为1
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

# 导入回归决策树模型DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor

depth = []
score = []

for i in range(1, 6):
    # 使用DecisionTreeRegressor函数，设置最大深度为i，随机参数为1,赋值给对象clf
    clf = DecisionTreeRegressor(max_depth=i, random_state=1)

    depth.append(i)

    # 对训练数据集及其目标变量进行训练
    clf.fit(x_train, y_train)

    # 计算出精确度
    temp = clf.score(x_test, y_test)

    score.append(temp)

# 导入matplotlib.pyplot模块进行可视化
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 绘制折线图
plt.plot(depth, score)

# 设置图标题为"树的深度与预测精度"
plt.title("树的深度与预测精度")

# 设置x轴标签为"回归决策树深度"
plt.xlabel("回归决策树深度")

# 设置y轴标签为"预测精确度"
plt.ylabel("预测精确度")

# 展示图片
plt.show()