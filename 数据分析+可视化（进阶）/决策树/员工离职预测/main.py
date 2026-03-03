import pandas as pd
df = pd.read_csv("员工信息表.csv")

# 使用replace()将"工资"列的低"，"中"，"高"替换为0，1，2
df["工资"] = df["工资"].map({'低': 0, '中': 1, '高': 2})
# 使用drop()函数删除"离职"列，剩余的数据作为自变量x
x = df.drop(columns="离职")

# 以二维结构读取"离职"列，作为因变量y
y = df[["离职"]]

# 导入sklearn.model_selection模块中的train_test_split函数
from sklearn.model_selection import train_test_split
# 使用train_test_split()函数划分训练集和测试集
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=123)

# 导入sklearn.tree模块中的分类决策树模型DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
# 使用DecisionTreeClassifier()初始化模型
model = DecisionTreeClassifier()

# 导入sklearn.model_selection模块中的GridSearchCV
from sklearn.model_selection import GridSearchCV
# 指定待调优参数max_depth的候选值范围，赋值给parameters
parameters = {'max_depth': [1 ,3, 5, 7, 9]}
# 使用GridSearchCV()函数进行参数调优，将结果赋值给grid_search
grid_search = GridSearchCV(model, parameters, scoring='roc_auc', cv=5)
# 传入训练集进行训练
grid_search.fit(x_train, y_train)
# 获取参数的最优值，并赋值给best_params
best_params = grid_search.best_params_

# 并设置参数max_depth=best_params,random_state=123
final_model = DecisionTreeClassifier(max_depth=best_params['max_depth'],random_state=123)
# 使用fit()函数训练模型
final_model.fit(x_train, y_train)

# 将x_test传入使用predict_proba()函数预测，将结果赋值给y_pred_proba
y_pred_proba = final_model.predict_proba(x_test)

# 导入sklearn.metrics模块中的roc_auc_score函数
from sklearn.metrics import roc_auc_score

# 将y_test和预测的离职概率传入roc_auc_score()，将结果赋值给auc_score
auc_score = roc_auc_score(y_test, y_pred_proba[:,1])

# 输出auc_score
print(auc_score)