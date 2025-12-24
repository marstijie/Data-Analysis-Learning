# 环境载入
from os.path import split

import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Line

# 通过F12获取弹幕xml网站
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'}
url = "https://comment.bilibili.com/29005054893.xml"
response = requests.get(url,headers=headers)

# 将request的编码方式调整为与网页编码格式一致防止乱码
response.encoding = response.apparent_encoding
#获取弹幕具体位置
xml = response.text
soup = BeautifulSoup(xml, "lxml-xml")
content_all = soup.find_all(name="d")
timeList = []
# for循环遍历content_all
for comment in content_all:
    # 将每条弹幕的时间给提取出来
    data = comment.attrs["p"]
    time = data.split(",")[0]
    timeList.append(float(time))
subtitlesDict={}
for i in range(46):
    start=60*i
    end=60*(i+1)
    segment_range=f'{start}-{end}'
    subtitlesDict[segment_range]=0
for subtitle in subtitlesDict.keys():
    start_key=subtitle.split('-')[0]
    end_key=subtitle.split('-')[1]
    for time in timeList:
        if int(start_key) <= time <= int(end_key):
            subtitlesDict[subtitle]+=1
#通过pyecharts实现可视化
line=Line()
line.add_xaxis(list(subtitlesDict.keys()))
line.add_yaxis("弹幕数",list(subtitlesDict.values()))
line.render('line.html')
print('success')