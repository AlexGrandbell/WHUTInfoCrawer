# 请先在官网查看所需页码返回，再直接运行输入即可。
from bs4 import BeautifulSoup
import requests
import pandas as pd

# 下载一个网页的html
def download_html(url):
    try:
        print("正在爬取网页:", url)
        r = requests.get(url)
        r.raise_for_status()  # 检查是否有HTTP错误
        r.encoding = "utf-8"
        print("成功")
        return r.text
    except requests.exceptions.RequestException as e:
        print("网页获取失败:", e)
        return None

# 获取所有网页信息，以列表形式返回所有html
def download_all_htmls(indexes):
    htmls = []
    #首页比较特殊
    if indexes[0] == 1 :
        url = "http://i.whut.edu.cn/xxtg/index.shtml"
        html_text = download_html(url)
        htmls.append(html_text)
    else:
        url = f'http://i.whut.edu.cn/xxtg/index_{indexes[0]-1}.shtml'
        html_text = download_html(url)
        htmls.append(html_text)
        
    for index in indexes:
        url = f'http://i.whut.edu.cn/xxtg/index_{index}.shtml'
        html_text = download_html(url)
        htmls.append(html_text)
    return htmls

# 解析单个HTML数据
def parse_single_html(html):
    soup = BeautifulSoup(html, "html.parser")
    datas = []  # 返回的数据
    list_items = soup.find("ul", class_="normal_list2").find_all("li") # 获得第一层数据，是一个列表
    for item in list_items:
        date = item.find("strong").get_text()
        title = item.find("a",title = True).get("title")
        lasthref = item.find("a",title = True).get("href")
        href = "http://i.whut.edu.cn/xxtg" + lasthref[1:]#合成真实地址
        dpm = item.find("a",title=False).get_text()

        datas.append({
            "发布日期":date,
            "部门":dpm,
            "标题":title,
            "URL":href
        })

    return datas

# 网页名称有规律，第一页是http://i.whut.edu.cn/xxtg/index.shtml，后面是http://i.whut.edu.cn/xxtg/index_{1-末位数}.shtml
start = int(input("请输入开始页码(1开始，不要超过范围):"))
end = int(input("请输入结束页码(1开始，不要超过范围):"))
page_indexes = range(start, end)
# page_indexes = range(1, 490)#默认范围
list(page_indexes)
info_htmls = download_all_htmls(page_indexes)

all_datas = []
for html in info_htmls:
    all_datas.extend(parse_single_html(html))

df = pd.DataFrame(all_datas)
df.to_excel("校园网数据.xlsx")
print("校园网数据.xlsx已经在此文件夹下生成")

#询问用户是否需要根据指定一个关键词筛选并生成另一个文件
#循环询问
while True:
    key = input("是否需要继续根据关键词筛选数据并生成文件？(y/n):")
    if key == "y":
        key_word = input("请输入关键词:")
        df_key = df[df["标题"].str.contains(key_word)]
        df_key.to_excel(f"校园网数据_{key_word}.xlsx")
        print(f"校园网数据_{key_word}.xlsx已经在此文件夹下生成")
    elif key == "n":
        break
    else:
        print("输入错误，请重新输入")
        continue