# 环境导入
import pandas as pd
import matplotlib.pyplot as plt

# 读取文件
df=pd.read_csv('ramenRatings.csv')

# 设置字体
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 计算品牌数量总和，根据品牌数量总和，选出排名前5的行数据
df['number']=df['Bowl']+df['Cup']+df['Pack']
df=df.sort_values('number',ascending=False)
dfend=df.head(5)
dfend.plot.bar('Area',['Bowl','Cup','Pack'])


plt.xticks(rotation=0)
plt.xlabel('国家/地区')
plt.ylabel('品牌总量')
plt.legend(loc='upper left')
plt.twinx()
plt.plot(dfend['Area'],dfend['rating'],marker='*',color='crimson',label='整体拉面评分')
plt.ylabel('评分')
plt.legend()
plt.show()