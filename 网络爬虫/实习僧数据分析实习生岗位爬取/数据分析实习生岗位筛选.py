# 加载环境
import requests
from bs4 import BeautifulSoup
import time
from pyecharts.charts import Bar

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"}

#分析前10页的所有岗位，浏览页面中信息显示不全，故选择进入每个岗位的具体网页
# 因为不止1页url，根据DRY原则，故定义一个新函数获取页面内的信息
def getPositionInfo(detail_url):
    res = requests.get(detail_url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, "lxml")

    # 找到岗位名称的节点
    job = soup.find(class_="new_job_name").span.string

    # 找到公司名称的节点
    companyName = soup.find(class_="com-name").string.strip()

    # 找到工作地址的节点
    position = soup.find(class_="job_position").string

    # 找到工作薪资的节点
    salary = soup.find(class_="job_money cutom_font").string

    # 使用with...as配合open()函数以a方式，打开路径为"/Users/tongtong/职位数据.txt"的文件，并赋值给f
    with open("数据分析实习生职位数据.txt", "a", encoding="utf-8") as f:

        # 使用write()函数写入job,companyName,position,salary
        f.write(job + "," + companyName + "," + position + "," + salary + "\n")


# for循环遍历range()函数生成的1-10的数字
for i in range(1, 11):
    url = f"https://www.shixiseng.com/interns?page={i}&type=intern&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%AE%9E%E4%B9%A0%E7%94%9F&area=&months=&days=&degree=&official=entry&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend="
    res = requests.get(url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    titles = soup.find_all(class_="title ellipsis font")
    for item in titles:
        detail_url = item.attrs["href"]

        # 调用getPositionInfo()函数，传入参数detail_url
        getPositionInfo(detail_url)

    # 每次爬取数据停顿2秒，免得短时间发送请求过多被拒绝
    time.sleep(2)

# 使用with...as语句配合open()函数以r方式，打开文件，赋值给f
with open("数据分析实习生职位数据.txt", "r",encoding="utf-8") as f:
    dataList = f.readlines()
cityDict = {}

#遍历整个txt文件
for data in dataList:
    # 去除无效薪资-"薪资面议"
    if "薪资面议" in data:
        continue
    city = data.split(",")[2]
    salary = data.split(",")[3]
    daily = salary.split("/")[0]
    if '-' in daily:
        start = daily.split("-")[0]
        end = daily.split("-")[1]
        average = (int(start)+int(end))/2
    else:
        average = int(daily)

    #将不同城市的岗位的平均薪资都添加到同一个key对应的列表中去
    if city not in cityDict.keys():
        cityDict[city] = []
    cityDict[city].append(average)

# 计算各城市的平均薪资
city_num_dict = {}
for key,value in cityDict.items():
    average_value = sum(value)//len(value)
    cityDict[key] = average_value
    #计算城市岗位数量
    city_num_dict[key] = len(value)

# 绘制各城市平均薪资的柱状图
bar = Bar()
bar.add_xaxis(list(cityDict.keys()))
bar.add_yaxis("平均薪资",list(cityDict.values()))
bar.render("salary.html")

# 绘制各城市职位数量的柱状图
bar_city = Bar()
bar_city.add_xaxis(list(city_num_dict.keys()))
bar_city.add_yaxis("职位数量",list(city_num_dict.values()))
bar_city.render("positions.html")