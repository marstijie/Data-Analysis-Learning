# 导入pandas
import pandas as pd

# 读取文件
data = pd.read_csv("住户信息.csv")

# 将data["身份证号"]转换为str类型
data["身份证号"] = data["身份证号"].astype(str)

# 创建储存性别的空列表
gender = []

# 使用for循环遍历data["身份证号"]
for num in data["身份证号"]:

    # 将身份证号的第13位转换为int
    num = int(num[12])

    # 如果num是奇数，列表中添加"男"
    if num % 2 == 1:
        gender.append("男")

    # 如果num是偶数，列表中添加"女"
    else:
        gender.append("女")

data['性别'] = gender

print(data)