# 导入模块
import pandas as pd

# 读取文件
df=pd.read_csv('180101-190630交易数据.csv')

# 将id作为索引
df=df.set_index('id')

# 处理异常值

# 删除order_id的异常值、重复值所在行
df.drop(df[df['order_id']<=0].index, inplace=True)
df= df.drop_duplicates('order_id')

# 删除user_id的异常值所在行
df.drop(df[df['user_id']<=0].index, inplace=True)

# 删除payment的异常值所在行
df.drop(df[df['payment']<0].index, inplace=True)

# 将payment列转化成单位元
df['payment']=df['payment']/100

# 删除price的异常值所在行
df.drop(df[df['price']<0].index, inplace=True)

# 将price列转化成单位元
df['price']=df['price']/100

# 删除items_count的异常值所在行
df.drop(df[df['items_count']<0].index, inplace=True)

# 删除cutdown_price的异常值所在行并转化成单位元
df.drop(df[df['cutdown_price']<0].index, inplace=True)
df['cutdown_price']=df['cutdown_price']/100

# 删除post_fee的异常值所在行并转化成单位元
df.drop(df[df['post_fee']<0].index, inplace=True)
df['post_fee']=df['post_fee']/100

# create_time，pay_time，转化成时间格式
df['create_time']=pd.to_datetime(df['create_time'])
df['pay_time']=pd.to_datetime(df['pay_time'])

# 删除create_time>pay_time的异常值
df.drop(df[df['create_time']>df['pay_time']].index, inplace=True)

# 快速浏览数据集
df.info()