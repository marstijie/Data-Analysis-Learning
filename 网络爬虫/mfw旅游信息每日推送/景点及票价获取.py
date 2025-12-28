# 载入坏境
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
}

# 景点名称及价格
nameList = []
priceList = []

#获取前5页内容
for page in range(1, 6):
    url2 = f"https://travelsearch.fliggy.com/index.htm?spm=181.61408.a1z7d.6.647523e4uB0Fd3&searchType=product&keyword=%E4%B8%8A%E6%B5%B7&category=SCENIC&ttid=seo.000000576&pagenum={page}"
    res = requests.get(url2, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    tourist_wraps = soup.find_all(class_="product-wrap clear-fix")
    for item in tourist_wraps:
        title = item.find(class_="main-title").string
        title_str = str(title)
        if title_str[0] != "[":
            # 就把title_str添加进列表nameList中
            nameList.append(title_str)
            price_item = item.find(class_="price")
            child = price_item.contents[1]
            priceList.append(child)
    time.sleep(2)

# 先将获取的列表信息转换成字典类型
total = {"景点名称": nameList, "景点价格/元": priceList}

info1 = pd.DataFrame(total)
writer1 = pd.ExcelWriter("城市景点.xlsx", mode="a", engine="openpyxl")
info1.to_excel(writer1, sheet_name="上海景点")

# 使用save()函数保存文档
writer1.close()