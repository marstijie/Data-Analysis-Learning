# 环境载入
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

House_type=[]
community_Address=[]
Building_Information=[]
per_price=[]
total_price=[]
writer=pd.ExcelWriter("二手房.xlsx")
for i in range(1,6):
    url=f"https://nocturne-spider.baicizhan.com/practise/61/PAGE/{i}.html"
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"}
    res=requests.get(url,headers=headers)
    html=res.text
    soup=BeautifulSoup(html,"lxml")
    content_all=soup.find_all('li',class_="clear")
    for content in content_all:
        type_=content.find('div',class_="info clear").find(class_="title").a.text.strip().replace('\n', '').replace('\r', '')
        House_type.append(type_)
        address_=content.find(class_='address').find(class_='flood').find(class_="positionInfo").a.text.strip().replace('\n', '').replace('\r', '')
        community_Address.append(address_)
        info=content.find(class_='address').find(class_="houseInfo").text.strip().replace('\n', '').replace('\r', '')
        Building_Information.append(info)
        price=content.find(class_='address').find(class_="priceInfo").find(class_="unitPrice").span.text.strip().replace('\n', '').replace('\r', '')
        per_price.append(price)
        pri=content.find(class_='address').find(class_="priceInfo").find(class_="totalPrice totalPrice2").text.strip().replace('\n', '').replace('\r', '')
        total_price.append(pri)
    time.sleep(2)

total={"房屋户型":House_type,"小区地址":community_Address,"建筑信息":Building_Information,"单价价格(元/平方)":per_price,"房子总价/万":total_price}
info=pd.DataFrame(total)
info.to_excel(writer,sheet_name="成都")
writer.close()