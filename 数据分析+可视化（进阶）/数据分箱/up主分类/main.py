import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("bilibili.csv")
data["date"] = pd.to_datetime(data["date"])

data = data.groupby(data["author"]).agg(
    coins=("coins", "sum"),
    danmu=("danmu", "sum"),
    favorite=("favorite", "sum"),
    likes=("likes", "sum"),
    reply=("reply", "sum"),
    view=("view", "sum"),
    video=("分区", "count"),
    max_date=("date", "max"),
    min_date=("date", "min")
)
data = data[data["video"] >= 5]

# 计算IFL
I = (data["danmu"] + data["reply"]) / data["view"] / data["video"] * 100
F = (data["max_date"] - data["min_date"]).dt.days / data["video"]
L = (data["likes"] + data["coins"] + data["favorite"]) / data["view"]

df = pd.concat([I, F, L], axis=1)
df.columns = ["I", "F", "L"]

df['I'] = pd.qcut(df["I"], q=5, labels=[1, 2, 3, 4, 5])
df['F'] = pd.qcut(df["F"], q=5, labels=[5, 4, 3, 2, 1])
df['L'] = pd.qcut(df["L"], q=5, labels=[1, 2, 3, 4, 5])


def getTrans(x):
    if x > 3:
        return 1
    else:
        return 0


df["I"] = df["I"].apply(getTrans)
df["F"] = df["F"].apply(getTrans)
df["L"] = df["L"].apply(getTrans)

df["mark"] = df["I"].astype(str) + df["F"].astype(str) + df["L"].astype(str)


def getType(x):
    if x == "111":
        return "高质量UP主"
    elif x == "101":
        return "高质量拖更UP主"
    elif x == "011":
        return "高质量内容高深UP主"
    elif x == "001":
        return "高质量内容高深拖更UP主"
    elif x == "110":
        return "接地气活跃UP主"
    elif x == "100":
        return "接地气UP主"
    elif x == "010":
        return "活跃UP主"
    else:
        return "还在成长的UP主"


df["type"] = df["mark"].apply(getType)
df_type = df["type"].groupby(df["type"]).count() / len(data)

plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

plt.bar(df_type.index, df_type.values)
plt.xticks(rotation=45)

plt.show()