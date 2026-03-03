import pandas as pd
df = pd.read_csv("multiple_to_new.csv")

# 以二维结构读取"exposure","hot","search"这三列，作为自变量x
x = df[["exposure", "hot", "search"]]
# 以二维结构读取"new_user"，作为因变量y
y = df[["new_user"]]

# 导入sklearn.linear_model模块中的LinearRegression函数
from sklearn.linear_model import LinearRegression

# 使用LinearRegression()初始化模型，赋值给lr_model
lr_model = LinearRegression()
# 使用lr_model模型的fit()函数，训练模型
lr_model.fit(x,y)

# 曝光量，搜索热度，关键词搜索量依次为300000,10000,30000
# 将300000,10000,30000以二维结构传入传入predict()函数进行预测，并赋值给 y_predict
y_predict = lr_model.predict([[300000,10000,30000]])

# 输出预测结果y_predict
print(y_predict)