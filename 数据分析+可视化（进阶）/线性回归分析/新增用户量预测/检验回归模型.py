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

# 将x,y传入score( )函数，对模型打分,获取判定系数r2
r2 = lr_model.score(x,y)
# 输出r2
print(r2)