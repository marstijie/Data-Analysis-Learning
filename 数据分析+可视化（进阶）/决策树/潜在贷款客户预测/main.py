# 导入pandas模块
import pandas as pd

# 读取数据
df = pd.read_csv('PersonalLoan.csv')

# 删除"是否接受贷款"和"用户编号"列，剩余的数据作为自变量x
x = df.drop(columns=["是否接受贷款","用户编号"])

# 以二维结构读取"是否接受贷款"列，作为因变量y
y = df[["是否接受贷款"]]

from sklearn.model_selection import train_test_split

#划分训练集和测试集
# 传入x和y，设置test_size为0.2,random_state为123
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)

from sklearn.tree import DecisionTreeClassifier

# 并设置参数max_depth=4,random_state=123，赋值给model
model = DecisionTreeClassifier(max_depth=4, random_state=123)

# 用训练集的x和y训练模型
model.fit(x_train, y_train)

# 预测
y_pred_proba = model.predict_proba(x_test)

from sklearn.metrics import roc_curve

fpr, tpr, thres = roc_curve(y_test, y_pred_proba[:, 1])

import matplotlib.pyplot as plt

# 绘制折线图
plt.plot(fpr, tpr)

plt.title("ROC")

plt.xlabel("FPR")

plt.ylabel("TPR")

plt.show()

from sklearn.metrics import roc_auc_score

auc_score = roc_auc_score(y_test, y_pred_proba[:,1])

print(auc_score)