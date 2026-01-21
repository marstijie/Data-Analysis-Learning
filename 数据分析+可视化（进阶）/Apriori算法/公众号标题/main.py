import pandas as pd

df = pd.read_csv("用户浏览数据.csv")

articles = []

for i in df['文章类型']:
    # 用将i的数据拆分，并将返回的列表赋值给article
    article = i.split(',')

    articles.append(article)


from apyori import apriori

# 进行关联分析
rules = apriori(articles, min_support=0.1, min_confidence=0.6)

# 创建空列表，用于存储关联规则等数据
extract_result = []

for rule in rules:
    #  提取支持度，保留3位小数
    support = round(rule.support, 3)

    for i in rule.ordered_statistics:
        # 获取前件和后件
        head_set = list(i.items_base)
        tail_set = list(i.items_add)
        # 跳过前件为空的数据
        if head_set == []:
            continue
        # 将前件、后件拼接成关联规则的形式
        related_category = str(head_set) + '→' + str(tail_set)
        # 提取置信度，保留3位小数
        confidence = round(i.confidence, 3)
        # 提取提升度，保留3位小数
        lift = round(i.lift, 3)
        # 将提取的数据保存到列表extract_result中
        extract_result.append([related_category, support, confidence, lift])
# 将数据转成DataFrame的形式，设置列名为'关联规则', '支持度', '置信度', '提升度'，并赋值给rule_data
rule_data = pd.DataFrame(extract_result, columns=['关联规则', '支持度', '置信度', '提升度'])
# 提取出提升度大于 1 的数据
promoted_rules = rule_data[rule_data['提升度'] > 1]
# 提取出提升度小于 1 的数据
restricted_rules = rule_data[rule_data['提升度'] < 1]

import matplotlib.pyplot as plt

# 字体设置
plt.rcParams["font.sans-serif"] = "Microsoft YaHei"

# 绘制簇形柱状图
# '关联规则' 列作为x轴数据，'支持度','置信度' 列作为y轴数据，参数rot=0
promoted_rules.plot.bar('关联规则',['支持度','置信度'],rot=0)

plt.title("促进关系的强关联规则")
plt.show()

restricted_rules.plot.bar('关联规则', ['支持度', '置信度'], rot=0)
plt.title("抑制关系的强关联规则")

plt.show()