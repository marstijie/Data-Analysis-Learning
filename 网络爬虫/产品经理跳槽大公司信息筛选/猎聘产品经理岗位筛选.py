import requests
from bs4 import BeautifulSoup

with open("工作数据.txt", "w", encoding="utf-8") as f:
    for page in range(1, 6):
        url = f"https://nocturne-spider.baicizhan.com/practise/42/PAGE/{page}.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        content_all = soup.find_all(class_="sojob-item-main clearfix")

        for content in content_all:
            # 获取公司名称元素
            company_name = content.find(class_="company-name").a.text

            # 获取职位信息元素
            job_element = content.find(class_="job-info")
            job_name_tag = job_element.find('a')
            job_name = job_name_tag.text.strip()
            job_link = job_name_tag.get("href", "")

            # 添加筛选条件：只写入"已上市"公司的数据
            financing = content.find(class_="field-financing")
            if financing and financing.span and financing.span.text == "已上市":
                f.write(f"{company_name},{job_name},{job_link}\n")