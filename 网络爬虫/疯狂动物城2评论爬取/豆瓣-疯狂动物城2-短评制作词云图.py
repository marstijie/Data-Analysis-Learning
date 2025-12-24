# 环境配置
import requests
from bs4 import BeautifulSoup
import jieba
from pyecharts.charts import WordCloud

# 将豆瓣电影评论URL地址，赋值给变量url
url = "https://movie.douban.com/subject/26817136/comments?status=P"
#--------------获取User-Agent(F12-网络-F5-标头-最下方)---------------
# 将User-Agent以字典键对形式赋值给headers
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'}
# 将 url 和 headers参数，添加进requests.get()中，将字典headers传递headers参数，给赋值给response
response = requests.get(url, headers=headers)

# 将服务器响应内容转换为字符串形式，赋值给html
html = response.text

# 使用BeautifulSoup()传入变量html和解析器lxml，赋值给soup
soup = BeautifulSoup(html, "lxml")

# 使用find_all()查询soup中class="short"的节点，赋值给content_all（从网页F12可以看到所有评论都在class="short"的节点中）
content_all = soup.find_all(class_="short")

# 创建一个空白列表wordList
wordList = []

# for循环遍历content_all
for content in content_all:
    # 获取每个节点中标签内容，赋值给contentString
    contentString = content.string

    # 使用jieba.lcut()将contentString进行分词，赋值给words
    words = jieba.lcut(contentString)

    # 将列表wordList和列表words进行累加
    wordList = wordList + words

# 创建一个空白字典wordDict
wordDict = {}

#将词和词频以key：value形式放入字典中
for word in wordList:
    if word == ".." or word == "......":
        continue
    if len(word) > 1:
        if word not in wordDict:
            wordDict[word] = 1
        else:
            wordDict[word] += 1
#创建词云图
wordCloud=WordCloud()
wordCloud.add(series_name='',
              data_pair=list(wordDict.items()),
              word_size_range=[20,80])
wordCloud.render('wordcloud.html')
print('success')
