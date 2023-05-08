from src import parse
from src import update
from src.lib import get 


list = get.product_list()

datas = []

for i in list:
    data = parse.parse(i)
    datas.append(data)

parse.create_csv(datas)