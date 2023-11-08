import requests
from pyquery import PyQuery as pq
import json
import pandas as pd

# 定义要保存到CSV的列名
columns = ['title', 'place', 'msg', 'price', 'per_meter']

# 定义一个函数，用于爬取某网页
def get_a_page(url):
    result = requests.get(url)  # 发送HTTP GET请求获取网页内容
    doc = pq(result.text)  # 使用PyQuery解析HTML文档
    ul = doc('.sellListContent')  # 定位包含房源信息的<ul>元素
    divs = ul.children('.clear .info.clear').items()  # 遍历每个房源信息的<div>元素
    count = 0  # 用于计数
    titles = []  # 存储房源标题
    places = []  # 存储位置信息
    msgs = []  # 存储其他房源信息
    prices = []  # 存储总价
    per_meters = []  # 存储每平米单价
    for div in divs:
        count += 1
        title = div.children('.title a').text()  # 提取房源标题
        place = div.children('.address .flood .positionInfo a').text()  # 提取位置信息
        msg = div.children('.address .houseInfo ').text()  # 提取其他房源信息
        price = div.children('.address .priceInfo .totalPrice span').text().strip() # 提取总价
        per_meter = div.children('.address .priceInfo .unitPrice span').text().strip()  # 提取每平米单价
        dict = {
            'title': title,
            'place': place,
            'msg': msg,
            'price': price,
            'per_meter': per_meter
        }

        titles.append(title)  # 将提取的数据添加到相应的列表中
        places.append(place)
        msgs.append(msg)
        prices.append(price)
        per_meters.append(per_meter)
        print(str(count) + ': ' + json.dumps(dict, ensure_ascii=False))  # 打印每个房源的数据

    datas = {
        'title': titles,
        'place': places,
        'msg': msgs,
        'price': prices,
        'per_meter': per_meters
    }

    # 创建一个Pandas DataFrame来存储数据，并追加到CSV文件中
    df = pd.DataFrame(data=datas, columns=columns)
    df.to_excel('ty.xlsx', index=False, header=False)

if __name__ == '__main__':
    # 主程序入口
    for i in range(1, 101):
        get_a_page(f'https://ty.ke.com/ershoufang/pg{i}/mw112/')# mw112是加了筛选数据的网址

