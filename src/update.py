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
    elif(category == "cpu"):
        data = update_cpu()

    for i in data:
        for j in jd:
            if(i["name"] == j["name"]):
                i["price"] = j["price"]
    
    for j in jd:
        if(j["category"] == category):
            jd.remove(j)

    
    product_data = jd + data 
    f = open("data/products.json",mode= "w")
    json.dump(product_data, f, indent=4)    
    f.close()

def make_dict_l(name,category,param):
    key = list(param.keys())[0]
    value = param.get(key)[0]
    dict = {"name" : name,"category" : category ,"price" : "", "param" :{key : value,"pdf_so":"p1"}}
    return dict

def make_dict_p(name,category,url):
    dict = {"name":name,"category":category,"price" : "", "url":url}
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
            dict = make_dict_l(name,category,param)
            dicts.append(dict)
    
    
    return dicts


def update_cpu():
    intel_data = requests.get("https://kakaku.com/pc/cpu/itemlist.aspx?pdf_Spec103=12,13&pdf_so=p2")
    data = intel_data.content.decode("shift-jis")
    data = html.fromstring(data)
    category = "cpu"
    dicts = []

    Intel = data.xpath("/html/body/div[1]/div/div[1]/div[5]/div[1]/div/form/table[2]/tbody/tr")[3:]
    amd_data = requests.get("https://kakaku.com/pc/cpu/itemlist.aspx?pdf_Spec103=103,104&pdf_so=p2")
    data = amd_data.content.decode("shift-jis")
    data = html.fromstring(data)
    
    AMD = data.xpath("/html/body/div[1]/div/div[1]/div[5]/div[1]/div/form/table[2]/tbody/tr")[3:]

    product_list = [Intel,AMD]

    for p in product_list:
        data = p[0].xpath("//a[contains(@class, 'ckitanker')]")
        
        for i in range(len(data)):
            url = data[i].get("href")
            name = data[i].xpath("text()")[0]

            dict = make_dict_p(name,category,url)
            dicts.append(dict)
    return dicts