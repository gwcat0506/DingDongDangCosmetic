from selenium import webdriver
from bs4 import BeautifulSoup as bs
import csv
import re
import time
from datetime import datetime
import time
import sys, os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import math

if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(chromedriver_path)
else:
    driver = webdriver.Chrome()
cat_id = [100000100010008,100000100010009,100000100010010,100000100090001,100000100090002,100000100090003,100000100100001,100000100100002,100000100100003,100000100110001,100000100110002,100000100080008,100000100080009,100000100080010,100000100080011,100000100080006,100000100080005,100000100080004,100000100020006,100000100020001,100000100020007,
100000100120001,100000100120002,100000100120003,100000100030012,100000100030004,100000100030008,100000100030006,100000100030005,100000100030013,100000100030007,
100000100040008,100000100040007,100000100040004,100000100040009,100000100040010,100000100040011,100000100040012,100000100040013,100000100050004,100000100050003,
100000100050002,100000100060005,100000100060003,100000100060004,100000100060001,100000100060002,100000100070007,100000100070008,100000100070009,100000100070010,
100000100070011,100000100070012,100000100070015,100000100070016,100000200030001,100000200030005,100000200030002,100000200030003,100000200030006,100000200030007,
100000200010015,100000200010024,100000200010023,100000200010022,100000200010021,100000200010020,100000200010019,100000200010018,100000200010017,100000200010016,
100000200020020,100000200020024,100000200020023,100000200020022,100000200020021,100000300030001,100000300030002,100000300030003,100000300030004,100000300040002,
100000300040004,100000300040001,100000300040003,100000300040005,100000300050001,100000300050002,100000300050003,100000300050004,100000300050005,100000300050006,
100000300050007,100000300050008,100000300050009]
for id in cat_id:
    print(id)
    list_title=[]
    list_price=[]
    list_pro_num=[]
    base_url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=' + str(id)
    driver.get(base_url)
    driver.implicitly_wait(5)
    product_num = driver.find_element_by_xpath('// *[ @ id = "Contents"] / p / span').text

    page_num = float(product_num)/24
    page_num = math.ceil(page_num)
    print(page_num)
    for num in range(page_num):
        new_url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=' + str(id) + '&fltDispCatNo=&prdSort=01&pageIdx=' + str(num+1)
        print(new_url)
        driver.get(new_url)
        driver.implicitly_wait(20)
        soup = bs(driver.page_source, 'html.parser')
        name_list = soup.find_all(class_ = 'tx_name')
        price_list = soup.find_all(class_='prd_price')
        pro_num_list = soup.find_all(class_ = 'btn_zzim jeem')
        for i in name_list:
            # try:
            title=i.text
            list_title.append(title)
            # print(title)
        for price in price_list:
            price = price.text
            price = price.replace("원", "")
            price = price.replace(",", "")
            if len(price) > 6:
                price=price[:6]
            list_price.append(price)
            # print(price)
        for pro_num in pro_num_list:
            pro_num = pro_num.get('data-ref-goodsno')
            list_pro_num.append(pro_num)
            # print(pro_num)

        for name,price,pro_num in zip(list_title,list_price,list_pro_num):
            f3 = open('올리브영 상품 데이터.csv', 'a+', newline='', encoding="euc-kr", errors='ignore')
            wr3 = csv.writer(f3)
            link='https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo='+str(pro_num)
            print(name,price,pro_num,link)
            wr3.writerow([name,price,pro_num,link])
            f3.close()






