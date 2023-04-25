from src import parse
from src import update
from src.lib import get 

list = get.product_list()

for i in list:
    parse.parse(i)
    