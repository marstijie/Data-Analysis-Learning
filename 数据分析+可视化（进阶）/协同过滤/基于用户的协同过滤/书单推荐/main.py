import pandas as pd
df = pd.read_csv('BookRates.csv')
userRating = df.pivot_table(index = 'ISBN',columns = 'user_id',values = 'rating')
corrmat = userRating.corr(method = 'pearson',min_periods = 5)
usercorr = corrmat[638].drop(index = 638)
mostcorr = usercorr.idxmax()
targetBook = userRating[mostcorr]
targetBook = targetBook[targetBook.values> 8]
user1Rating = userRating[638].dropna()
targetName = targetBook.index
userName = user1Rating.index
bookList = targetName[~targetName.isin(userName)].values
print(bookList)