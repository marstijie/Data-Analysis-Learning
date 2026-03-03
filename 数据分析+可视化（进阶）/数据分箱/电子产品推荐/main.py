import pandas as pd

# 读取文件
df = pd.read_csv("electronic.csv", encoding='utf-8')

# 一、计算{电视}的支持度
# 获取电视这一列数据
tv = df["电视"]

# 对数据中每个值进行计数和排序
tv = tv.value_counts()

# 获取购买电视的订单数量
tv_cnt = tv[1]

tv_support = tv_cnt / 13

# 二、计算{游戏机}的支持度
# 获取游戏机这一列数据
game = df["游戏机"]

# 对数据中每个值进行计数和排序
game = game.value_counts()

# 获取购买游戏机的订单数量
game_cnt = game[1]

game_support = game_cnt / 13

# 三、计算{电视,游戏机}的支持度
# 既购买了电视又购买了游戏机的数据
tv_game = df[(df["游戏机"] == 1) & (df["电视"] == 1)]

# 获取"游戏机"这一列
data = tv_game["游戏机"]

# 统计这列订单数量
cnt = data.count()

tv_game_support = cnt / 13

# 四、计算{电视}→{游戏机}的置信度
tv_game_confidence = tv_game_support / tv_support

# 五、计算{电视}→{游戏机}的提升度

tv_game_lift = (tv_game_support / (tv_support * game_support)).round(1)

# 六、输出结果
# 根据提升度是否大于1来格式化输出结果

if tv_game_lift > 1:

    print(f"电视对游戏机的提升度为{tv_game_lift}，能推荐")

else:

    print(f"电视对游戏机的提升度为{tv_game_lift}能推荐")