from bs4 import BeautifulSoup
import requests

# 主页面URL
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
           "cookie":"Hm_lvt_ab8ddafbce3f7ff86be6f2ab9bf24d48=1766493493"}
main_url = "https://nocturne-spider.baicizhan.com/practise/31.html"
main_html = requests.get(main_url,headers=headers).text
main_soup = BeautifulSoup(main_html, 'html.parser')
# 存储已下载图片（记录每个基础名称出现的总次数）
downloaded = {}
# 记录每个基础名称是否重复
is_duplicate = {}

# 第一步：先统计每个文件名出现的总次数
for img in main_soup.find_all('img', alt=True):
    img_alt = img['alt']
    filename_base = img_alt.replace(' ', '_')

    if filename_base not in downloaded:
        downloaded[filename_base] = 0
        is_duplicate[filename_base] = False

    downloaded[filename_base] += 1
    # 如果出现次数超过1次，标记为重复
    if downloaded[filename_base] > 1:
        is_duplicate[filename_base] = True

# 重置计数器用于生成文件名
name_counters = {}

# 第二步：再次遍历并下载图片
count = 0
for img in main_soup.find_all('img', alt=True):
    # 从img标签获取alt作为文件名
    img_alt = img['alt']
    filename_base = img_alt.replace(' ', '_')

    # 初始化计数器
    if filename_base not in name_counters:
        name_counters[filename_base] = 0

    name_counters[filename_base] += 1

    # 只有重复的文件名才加编码
    if is_duplicate[filename_base]:
        filename = f"{filename_base}-{name_counters[filename_base]}.jpg"
    else:
        filename = f"{filename_base}.jpg"

    # 查找包含此图片的href链接
    parent_link = img.find_parent('a', href=True)

    if parent_link:
        detail_url = parent_link['href']

        # 第二步：访问详情页获取高清图片
        try:
            detail_html = requests.get(detail_url,headers=headers).text
            detail_soup = BeautifulSoup(detail_html, 'html.parser')

            # 在详情页中查找高清图片
            hd_img = detail_soup.find('div', class_='pictureshow')
            if hd_img:
                img_tag = hd_img.find('img', src=True)
                if img_tag:
                    img_src = img_tag['src']

                    # 下载高清图片
                    with open(filename, 'wb') as f:
                        f.write(requests.get(img_src).content)

                    count += 1
                    print(f"已下载高清图片: {filename}")

        except:
            continue

print(f"完成！共下载 {count} 张高清图片")