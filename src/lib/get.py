import requests
import json


def get_data(product_name):
    #指定したサイトの生データを取得する
    
    url,param = get_url(product_name)

    data = requests.get(url,params=param)

    return data

def get_data_p(product_name):
    rpf = open("data/products.json")
    pf = json.load(rpf)

    #商品データ取得
    for pd in pf:
        if pd["name"] == product_name:
            product_data = pd
            break
    
    url = product_data["url"]
    data = requests.get(url)
    return data

def get_url(product_name):
    #商品名からurlを返す
    
    #データ取り込み
    rpf = open("data/products.json")
    pf = json.load(rpf)
    ruf = open("data/urls.json")
    uf = json.load(ruf)

    #商品データ取得
    for pd in pf:
        if pd["name"] == product_name:
            product_data = pd
            break

    #url形成
    category = product_data["category"]
    directory_path = uf[category]
    url = f"https://kakaku.com{directory_path}/itemlist.aspx"
    param = product_data["param"]

    return url,param

def get_product_entry(product_name):
    #データ取り込み
    rpf = open("data/products.json")
    pf = json.load(rpf)

    #商品データ取得
    for pd in pf:
        if pd["name"] == product_name:
            product_data = pd
            break

    return product_data

def set_price(product_data):
    rpf = open("data/products.json")
    pf = json.load(rpf)
    rpf.close()
    for pd in pf:
            if pd["name"] == product_data["name"]:
                pd["price"] = product_data["price"]
                break
    
    rpf = open("data/products.json","w")
    json.dump(pf,rpf,indent=4)

def product_list():
    rpf = open("data/products.json")
    pf = json.load(rpf)
    rpf.close()
    list = []
    for i in pf:
        list.append(i["name"])
    return list