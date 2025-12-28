# 载入坏境
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
}

writer = pd.ExcelWriter("美食排行.xlsx")

# 解析网页发现北京和上海对应的网页中的城市编码分别是10065和10099
for city in ["10065", "10099"]:

    # 定义列表title_list用于存储店铺名称
    title_list = []
    # 定义列表score_list用于存储评分
    score_list = []
    # 定义列表review_list用于存储点评数据
    review_list = []

    # 获取前5页美食内容
    for page in range(1, 6):

        # 使用time.sleep()控制，每次循环停顿1秒
        time.sleep(3)
        url1 = f"http://www.mafengwo.cn/cy/{city}/0-0-0-0-0-{page}.html"
        response = requests.get(url1, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        content_all = soup.find_all(class_="item clearfix")
        for content in content_all:
            content_grade = content.find(class_="grade")
            score = content_grade.em.string
            score_list.append(score)
            review = content_grade.p.em.string
            review_list.append(review)
            title = content.find(class_="title").h3.a.string
            title_list.append(title)

    # 先将获取的列表信息转换成字典类型
    total = {"名称": title_list, "评分": score_list, "点评数量": review_list}
    info = pd.DataFrame(total)

    # 使用if判断，遍历10065北京的编号时
    if city == "10065":
        info.to_excel(excel_writer=writer, sheet_name="北京美食")
    else:
        info.to_excel(excel_writer=writer, sheet_name="上海美食")

writer.close()
