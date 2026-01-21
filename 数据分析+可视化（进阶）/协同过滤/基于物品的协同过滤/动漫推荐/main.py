import pandas as pd

df = pd.read_csv("anime.csv", encoding="utf-8")

'''寻找相似的动漫'''

df = df[df["av_rating"]>7]

ratings = df.pivot_table(index="user_id", columns="name", values="rating")

# 计算不同动漫间的皮尔逊相关系数
corrMatrix = ratings.corr(method="pearson")

'''寻找铃可感兴趣的动漫'''

targetRatings = ratings.loc[1].dropna()

# 根据每一部铃可评分过的动漫，预测她对未评分动漫的感兴趣程度

name = targetRatings.index
score = targetRatings.values

sims = corrMatrix[name].drop(index=name)

prod = score * sims

animeList = prod.sum(axis=1)

'''获取可推荐动漫列表'''
# 将推荐列表降序排序,获取感兴趣程度最高的前3部动漫的名称
animeList = animeList.sort_values(ascending=False).index[0:3].values

print(animeList)