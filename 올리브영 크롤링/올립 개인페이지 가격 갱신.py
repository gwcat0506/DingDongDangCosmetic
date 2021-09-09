import csv
import os
import re
import sys
import time
import time
from datetime import datetime
import math
from bs4 import BeautifulSoup as bs
from selenium import webdriver

if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(chromedriver_path)
else:
    driver = webdriver.Chrome()

list_title=[]
list_price=[]
list_pro_num=[]
base_url='https://www.oliveyoung.co.kr/store/main/getSaleList.do'
driver.get(base_url)
product_num = driver.find_element_by_xpath('//*[@id="Container"]/div[2]/div[3]/p/span').text
product_num = product_num.replace(',','')
page_num = float(product_num)/300
page_num = math.ceil(page_num)
print(page_num)
for num in range(page_num):
    new_url = 'https://www.oliveyoung.co.kr/store/main/getSaleList.do?dispCatNo=900000100090001&fltDispCatNo=&prdSort=01&pageIdx=' + str(num+1) +'&rowsPerPage=300'
    driver.get(new_url)
    time.sleep(5)
    driver.implicitly_wait(5)
    soup = bs(driver.page_source, 'html.parser')
    price_list = soup.find_all(class_ = 'tx_cur')
    pro_num_list = soup.find_all(class_ = 'btn_zzim jeem')
    for price in price_list:
        price = price.text
        price = price.replace("원", "")
        price = price.replace(",", "")
        list_price.append(price)

    for pro_num in pro_num_list:
        pro_num = pro_num.get('data-ref-goodsno')
        list_pro_num.append(pro_num)

    for price, pro_num in zip( list_price, list_pro_num):
        f3 = open('올리브영 세일 데이터.csv', 'a+', newline='', encoding="euc-kr", errors='ignore')
        wr3 = csv.writer(f3)
        print(price, pro_num)
        wr3.writerow([price, pro_num])
        f3.close()