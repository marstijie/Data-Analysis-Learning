# 环境载入
import requests
from bs4 import BeautifulSoup

# 将User-Agent以字典键对形式赋值给headers
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'}

# 将前5页数据爬取下来
for i in range(5):
    #每翻一页start增加25
    page=i*25
    url=f'https://movie.douban.com/top250?start={page}&filter='
    response = requests.get(url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    #通过F12发现图片在class="pic"的节点
    content_all=soup.find_all('div',{'class':'pic'})
    for item in content_all:
        img=item.find('img')
        imgName=img.attrs['alt']
        imgUrl=img.attrs['src']
        #通过点击图片发现高清图片链接与原链接的区别为s_ratio_poster替换成l
        imgUrlHd=imgUrl.replace('s_ratio_poster','l')
        imgResponse=requests.get(imgUrlHd,headers=headers)
        img=imgResponse.content
        with open(f'{imgName}.jpg','wb') as f:
            f.write(img)

