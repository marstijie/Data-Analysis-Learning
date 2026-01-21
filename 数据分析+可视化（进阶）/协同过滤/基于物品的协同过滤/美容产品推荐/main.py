import pandas as pd

df = pd.read_csv("Beauty_products.csv")

userRating = df.pivot_table(index="UserId", columns="ProductId", values="Rating")

corrMatrix = userRating.corr(method="pearson")

userList = list(userRating.index.values)
result = []

for i in userList:
    productRating = userRating.loc[i].dropna()

    name = productRating.index
    score = productRating.values

    sims = corrMatrix[name].drop(index=name)
    prod = score * sims

    productList = prod.sum(axis=1).sort_values(ascending=False).index[0:5].values
    result.append(productList)

print(pd.DataFrame({"用户ID": userList, "推荐列表": result}))
