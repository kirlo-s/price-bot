from src.lib import get
from lxml import html

def parse(product_name):
    data = get.get_data(product_name).content.decode("shift-jis")
    html_data = html.fromstring(data)
    
    #取得階層
    path_root = "/html/body/div[1]/div/div[1]/div[5]/div[1]/div/form/table[2]/tbody/tr[5]"
    path_price_data = "/td[2]/ul/li[1]/a"
    path_store_data = "/td[2]/ul/li[2]/text()[1]"
    path_img = "/td[1]/a/img"
    
    #マスターデータの作成
    price_data = html_data.xpath(path_root + path_price_data)[0]
    store_data = html_data.xpath(path_root+path_store_data)[0]
    img_data = html_data.xpath(path_root + path_img)[0]

    #値の取得
    price = price_data.text
    price = price.replace(',', '')
    price = price.replace("¥","")
    price = int(price)

    url = price_data.get("href")
    store = store_data
    img = img_data.get("src")

    p_data = {"name" : product_name,"price":price,"price_before": None,"url":url,"store":store,"img":img}

    p_data["price_before"]= get.set_price(p_data)
    return p_data