import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("diabetes.csv")

# 计算数据相关矩阵
corr = df.corr(method="pearson")

# 绘制热力图，设置颜色为"RdBu"，形状为方形，显示数字标记
sns.heatmap(corr, cmap="RdBu", square=True, annot=True)

plt.show()


targetcorr = corr["target"]
targetcorr = targetcorr[(targetcorr.abs()>0.1) & (targetcorr.abs()<1)].index

# 自变量
x = df[targetcorr]

# 因变量
y = df[["target"]]

from statsmodels.stats.outliers_influence import variance_inflation_factor

for i in x.columns:
    VIF = variance_inflation_factor(x.values, x.columns.get_loc(i))
    if VIF > 10:
        x = x.drop(columns=i)

        # 划分数据集
from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.1,random_state=1)

# 拟合多重线性回归模型
from sklearn.linear_model import LinearRegression

lr_model = LinearRegression()

lr_model.fit(x_train, y_train)

b = lr_model.coef_[0][0].round(2)
c = lr_model.coef_[0][1].round(2)
d = lr_model.coef_[0][2].round(2)
e = lr_model.coef_[0][3].round(2)
f = lr_model.coef_[0][4].round(2)
g = lr_model.coef_[0][5].round(2)
h = lr_model.coef_[0][6].round(2)
i = lr_model.coef_[0][7].round(2)
a = lr_model.intercept_[0].round(2)

print(f"线性回归方程：Y={a}{b}X1+{c}X2+{d}X3{e}X4{f}X5+{g}X6+{h}X7+{i}X8")
