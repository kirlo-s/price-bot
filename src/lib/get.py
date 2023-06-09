import requests
import json


def get_data(product_name):
    #指定したサイトの生データを取得する
    
    url,param = get_url(product_name)

    data = requests.get(url,params=param)
    print(data.content.decode("shift-jis"))
    
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


