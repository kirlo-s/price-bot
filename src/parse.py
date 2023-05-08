from src.lib import get
from lxml import html
import csv

def parse(product_name):
    data = get.get_product_entry(product_name)
    print(product_name)
    if("param" in data):
        return parse_l(product_name)
    else:
        return parse_p(product_name)
    

def parse_l(product_name):
    data = get.get_data(product_name).content.decode("cp932")
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

    p_data = {"name" : product_name,"price":price,"url":url,"store":store,"img":img}

    get.set_price(p_data)
    return p_data


def parse_p(product_name):
    data = get.get_data_p(product_name).content.decode("cp932")
    html_data = html.fromstring(data)

    name = html_data.xpath("/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/div/div[1]/div[2]/div[1]/h2")[0].text
    img = html_data.xpath("/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/img")
    if(len(img) != 0):
        img = img[0].get("src")
    else:
        img = ""
    url = get.get_product_entry(product_name)["url"]
    store = html_data.xpath("/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[3]/span/a/text()")[0]
    
    price = html_data.xpath("/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/p/span")[0].text
    price = price.replace(',', '')
    price = price.replace("¥","")
    price = int(price)

    p_data = {"name" : product_name,"price":price,"url":url,"store":store,"img":img}

    return p_data

def create_csv(data):
    f = open("out.csv","w")
    writer = csv.writer(f)

    line = ["name","price","url","store"]
    writer.writerow(line)
    for d in data:
        line = [d["name"],str(d["price"]),d["url"],d["store"]]
        writer.writerow(line)