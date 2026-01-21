import pandas as pd
from apyori import apriori

df = pd.read_csv("TCM.csv", encoding="utf-8")

disease = []

for i in df["病人症状"]:
    x = i.split(",")
    disease.append(x)

result = []

rules = apriori(disease, min_support=0.1, min_confidence=0.7)

for rule in rules:
    support = round(rule.support, 3)
    for i in rule.ordered_statistics:
        head_set = list(i.items_base)
        if head_set == []:
            continue
        tail_set = list(i.items_add)
        related_category = str(head_set) + "→" + str(tail_set)
        confidence = round(i.confidence, 3)
        lift = round(i.lift, 3)
        result.append([related_category, support, confidence, lift])
data = pd.DataFrame(result, columns=["关联规则", "支持度", "置信度", "提升度"])

print(data[data["提升度"] > 1])