import pandas as pd

'''数据处理'''
# 读取并拼接数据集
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
movieRatings = pd.merge(ratings, movies)

'''构建模型'''
# 1. 构建「物品-用户数据透视表」
userRatings = movieRatings.pivot_table(index="电影名", columns="用户id", values="评分")

# 2. 计算用户间的相关系数
corrMatrix = userRatings.corr(method="pearson", min_periods=10)

# 3. 寻找相似用户
# 3.1 获取「用户1」与其他用户之间的皮尔逊相关系数
userCorr = corrMatrix[1].drop(index=1)

# 3.2 获取最大值对应的索引，并赋值给变量mostCorrUser
mostCorrUser = userCorr.idxmax()

# 4. 筛选可推荐电影
# 4.1 获取相似用户的电影评分数据
targetMovie = userRatings[mostCorrUser]

# 4.2 获取相似用户评分为5的电影
targetMovie = targetMovie[targetMovie.values==5]

# 4.3 获取目标用户评分过的电影数据
user1Ratings = userRatings[1].dropna()

# 4.4 删除目标用户看过的电影
# 获取相似用户评分为5的电影名称，并赋值给targetName
targetName = targetMovie.index

# 获取目标用户评分过的电影名称，并赋值给user1Name
user1Name = user1Ratings.index

# 筛选「用户1」未评分过的电影名称
movieList = targetName[~targetName.isin(user1Name)]

# 获取可推荐电影的名称
movieList = movieList.values

# 输出movieList
print(movieList)