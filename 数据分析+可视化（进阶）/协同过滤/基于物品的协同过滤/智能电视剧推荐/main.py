import pandas as pd

ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
result = pd.merge(ratings, movies)

user_movie = result.pivot_table(index="用户id", columns="电影名", values="评分")

corrMatrix = user_movie.corr(method="pearson")

user1Ratings = user_movie.loc[1].dropna()

name = user1Ratings.index
score = user1Ratings.values

simsMovie = corrMatrix[name].drop(index=name)

prod = score * simsMovie

movieList = prod.sum(axis=1)

movieList = movieList.sort_values(ascending=False)

movieList = movieList.index[0:5]

movieList = movieList.values

print(movieList)