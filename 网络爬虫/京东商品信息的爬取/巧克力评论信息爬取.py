# 环境载入
import requests
from bs4 import BeautifulSoup
import json
from pyecharts.charts import Bar

# 向网页发送请求，获取网页代码
url1 = "https://search.jd.com/Search?keyword=%E5%B7%A7%E5%85%8B%E5%8A%9B&enc=utf-8&wq=%E5%B7%A7%E5%85%8B%E5%8A%9B&pvid=dd65926ff30441409a11eceb998167db"

# 发现仅用User-Agent无法获取信息，尝试在headers中加入cookie
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
    "cookie": "__jdu=1760677046547424364008; shshshfpa=85ed560a-e4ad-4c0c-6bb0-4e72be4a8109-1760677080; shshshfpx=85ed560a-e4ad-4c0c-6bb0-4e72be4a8109-1760677080; TrackID=1Heb72NKAvEqINC3mO2e23Kkh9eKr4A5G9UjqhmI0LrJpWvPnpkZZ4DJMAYnyBla-2t8ZD1CV5YPCtk1ptRjig6O9gec3P6bY_aVYRXUT1fQ8cbvTfypUMT7pUzIR121-; light_key=AASBKE7rOxgWQziEhC_QY6yazWrH23sz58sa_g0fB_W_AhZKEG77Fx0VMftblFi-tjnyFuJc; pinId=pDDCMD5HClv8j_KvSNWTg3ilX2mRzija; pin=jd_rsVHVpdRvfdIATQ; unick=jd_1s8poj636gpvvs; __jdv=143920055|direct|-|none|-|1766740264031; o2State=; thor=894342F5DBF2AD7E52103AC4F2989684849931C9A55A7A11E8668A0696D9CF1E06C413CD9CF61D0C9C3DB3E04F435D67370D2CAB2A4BCA5BAAEE4C589ED0C54421F443EBD417AE8E7CD46ABC2F6671D08FB8CAF5061E451435EB464DE9EFB36B7ACB5CFAE560FEE3467875FBB9F242ABCBE5F88793178DF6C4B2919215A1438A6F28F87124A2AAD305ADCAD72B01150EDA0A8BAC506A4C7BE257741D6CA25A06; is_avif=onAVIF; 3AB9D23F7A4B3CSS=jdd032CFTQJ6EGNQARXFKUNGR6UENZJBZNJQATBL6QGEJGNQYRAPP7IEH5PPJHFYOQPURSFIUVLIDQ6UQVUMQWCI44YT3FQAAAAM3LHWQVAQAAAAADDAOZUMEJ66O6YX; areaId=22; cn=1; ipLoc-djd=1-72-55653-0; mail_times=4%2C1%2C1766740297555; flash=3_NhCOyI-MZ1BvVXr-nRdn9Y88V4Uj7anmp3rK0dSIYfA_8ybNKnIFxxGSQmpAQ9rUYehDtHgczwIqF1tirmYDgayC08Roy09h_cRKfDAY_wwoaN5E8YSKEL6FnBBQ7ZrKBPnu8HKZwm-mIZK2RUncrPKMmrhSDzJ6sAxQ1xC2g2Hf8MxBpop07pxh; PCSYCityID=CN_510000_510100_0; umc_count=1; __jda=143920055.1760677046547424364008.1760677046.1760677046.1766740264.2; __jdc=143920055; shshshfpb=BApXWEFblWv5AG_gaFuqiuNl5JwUFjDDTBiImd69p9xJ1INZfQpTFpDLdnC_IJYB3WpRshxkrQ8pVRIZm7K0O5o95M1u3-z6aEiPWRRE; 3AB9D23F7A4B3C9B=2CFTQJ6EGNQARXFKUNGR6UENZJBZNJQATBL6QGEJGNQYRAPP7IEH5PPJHFYOQPURSFIUVLIDQ6UQVUMQWCI44YT3FQ; sdtoken=AAbEsBpEIOVjqTAKCQtvQu17fCihFGneM4oJwRIa3KlbutWbsXj_Xo4IjmRy-H5tqNqnAodfhT7NXIkOG9E5YUE5pAI3GPzS2bUg0QDrA9JWoQxMe6MsuIpnAueRcD2sGgEIWDOSYOOLSM3xCddIhGGBu5VDiORiuSaeuL7EhCnh-aa5GFd74SuI0Dw; __jdb=143920055.10.1760677046547424364008|2.1766740264"
}
response = requests.get(url1, headers=headers)
html = response.text
soup = BeautifulSoup(html, "lxml")

# 分析网页，找到批量提取数据方法
# 进入商品页面后发现网址中仅有商品编码发生改变，而商品编码都储存在这个class中
content_all = soup.find_all(class_="gl-item")
comment_dict={}
for content in content_all:

    # 找到商品代码储存处data-sku
    p_id = content.attrs["data-sku"]

    # 评论均储存在JS文件中无法直接爬取，故复制储存评论的js文件的接口
    url2 = f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={p_id}'
    res = requests.get(url2, headers=headers)
    html = res.text

    # 解析网页，根据商品编号批量提取评论信息并保存
    html = html.lstrip("fetchJSON_comment98(")
    # 使用rstrip()移除右侧的);，赋值给html
    html = html.rstrip(");")
    # 使用json.loads()将str转换成dict型，赋值给json_data
    json_data = json.loads(html)

    # 观察json_data，发现所有商品评论信息都储存在"hotCommentTagStatistics"中
    data = json_data["hotCommentTagStatistics"]

    # 定义一个字典p_dict用于存放每个商品的标签信息
    p_dict = {}
    for item in data:
        name = item["name"]
        count = item["count"]
        p_dict[name] = count
    for content in p_dict.keys():
        if content not in comment_dict.keys():
            comment_dict[content] = 1
        else:
            comment_dict[content] += 1
bar= Bar()
bar.add_xaxis(list(comment_dict.keys()))
bar.add_yaxis('评价频次',list(comment_dict.values()))
bar.render("巧克力评论频次.html")