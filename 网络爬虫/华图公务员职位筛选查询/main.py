import requests
from bs4 import BeautifulSoup
import pandas as pd

city_list = []
department_list = []
branch_list = []
positionname_list = []
writer = pd.ExcelWriter("公务员职位信息.xlsx")
headers = {"user-agent"
           : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
for page in range(1, 6):
    url = f"https://nocturne-spider.baicizhan.com/practise/60/PAGE/{page}.html"
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    content_all = soup.find_all("tr")
    for content in content_all:
        items = content.find_all("td")
        if len(items) >= 4:
            city = items[0].string if items[0].string else items[0].get_text().strip()
            city_list.append(city)

            department = items[1].string if items[1].string else items[1].get_text().strip()
            department_list.append(department)

            branch = items[2].string if items[2].string else items[2].get_text().strip()
            branch_list.append(branch)

            positionname = items[3].string if items[3].string else items[3].get_text().strip()
            positionname_list.append(positionname)

total = {"地区": city_list, "部门": department_list, "用人司局": branch_list, "职位名称": positionname_list}
info = pd.DataFrame(total)
info.to_excel(writer, sheet_name="计算机科学与技术")
writer._save()