import json
import requests
from lxml import html 
from urllib.parse import urlparse,parse_qs

def update_products(category):

    f = open("data/products.json",mode = "r")
    jd = json.load(f)
    f.close()
    if(category == "videocard"):
        data = update_videocard()
    for i in data:
        for j in jd:
            if(i["name"] == j["name"]):
                i["price_before"] = j["price_before"]
    
    for j in jd:
        if(j["category"] == category):
            jd.remove(j)

    
    product_data = jd + data 
    f = open("data/products.json",mode= "w")
    json.dump(product_data, f, indent=4)    
    f.close()

def make_dict(name,category,param):
    key = list(param.keys())[0]
    value = param.get(key)[0]
    dict = {"name" : name,"category" : category ,"price_before" : "", "param" :{key : value,"pdf_so":"p1"}}
    return dict

def update_videocard():
    html_data = requests.get("https://kakaku.com/pc/videocard/itemlist.aspx")
    data = html_data.content.decode("shift-jis")
    data = html.fromstring(data)
    category = "videocard"
    dicts = []

    Nv_1 = data.xpath("/html/body/div[1]/div/div[1]/div[5]/div[2]/div[1]/div[5]/ul[1]/li")[1:]
    Nv_2 = data.xpath("/html/body/div[1]/div/div[1]/div[5]/div[2]/div[1]/div[5]/div[1]/div[1]/ul/li")
    AMD_1 = data.xpath("/html/body/div[1]/div/div[1]/div[5]/div[2]/div[1]/div[5]/ul[2]/li")[1:]
    AMD_2 = data.xpath("/html/body/div[1]/div/div[1]/div[5]/div[2]/div[1]/div[5]/div[2]/div[1]/ul/li")
    Intel = data.xpath("/html/body/div[1]/div/div[1]/div[5]/div[2]/div[1]/div[5]/ul[3]/li")[1:]
    
    
    product_list = [Nv_1,Nv_2,AMD_1,AMD_2,Intel] 
    for p in  product_list:   
        for i in range(len(p)):
            url = p[i].find("a").get("href")
            param = parse_qs(urlparse("https://kakaku.com/pc" + url).query)
            name = p[i].find("a").text
            dict = make_dict(name,category,param)
            dicts.append(dict)
    
    
    return dicts
