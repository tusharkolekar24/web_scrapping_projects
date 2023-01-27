import os
from selenium import webdriver
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time 

file_path= os.path.join(os.getcwd(),'web_scrapping_projects','finance_application','store_output','product.xlsx')
#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.amazon.in/s?k=mobiles&crid=9K8BD3OG7W34&sprefix=mobiles%2Caps%2C326&ref=nb_sb_noss_1')
driver.maximize_window()

go_next_page = s1 = driver.find_elements(by=By.XPATH, value='//span[@class="s-pagination-strip"]/a')
next_page_url =['https://www.amazon.in/s?k=mobiles&crid=9K8BD3OG7W34&sprefix=mobiles%2Caps%2C326&ref=nb_sb_noss_1']
for interation in go_next_page[:-1]:
    current_page = interation.get_attribute('href')
    next_page_url.append(current_page) 

myproduct_url =[]
for page_iteration in next_page_url:
    driver.get(page_iteration)
    time.sleep(2)
    
    page_urls = driver.find_elements(by=By.XPATH, value='//div[@class="aok-relative"]/span/a')
    
    for inter_page_url in page_urls:
        url_link = inter_page_url.get_attribute('href')
        myproduct_url.append(url_link)

driver = webdriver.Chrome(ChromeDriverManager().install())
my_prod_detail = []
title_details = []
add_details   = []
my_offer      = []
discounts     = []
myproduct_url = myproduct_url[:3]

for url_link,pr_no in zip(myproduct_url,range(len(myproduct_url))):
    print(pr_no)
    try:
        
        driver.get(url_link)
        driver.maximize_window()
        #time.sleep(1)
        title = driver.find_elements(by=By.XPATH, value='//h1[@class="a-size-large a-spacing-none"]')
        prod_detail = driver.find_elements(by=By.XPATH, value='//table[@class="a-normal a-spacing-micro"]/tbody/tr')
        other_details = driver.find_elements(by=By.XPATH, value='//ul[@class="a-unordered-list a-vertical a-spacing-mini"]/li/span')
        offers        = driver.find_elements(by=By.XPATH, value='//div[@class="a-cardui vsx__offers-holder"]')
        discount      = driver.find_elements(by=By.XPATH, value='//div[@class="a-section a-spacing-none aok-align-center"]/span')
        
        my_prod_detail.append([f.text for f in prod_detail])
        title_details.append(title[0].text)
        add_details.append([f.text for f in other_details])
        my_offer.append([f.text.split('\n') for f in offers])
        discounts.append([f.text for f in discount])
        
    except:
          pass
    #break

table_p_details = pd.DataFrame(my_prod_detail)
table_p_details.columns=[f'product_details_{f}' for f in range(table_p_details.shape[1])]
table_p_details.index = np.arange(0,table_p_details.shape[0])

table_title = pd.DataFrame(title_details,columns=['Title'])
table_title.index = np.arange(0,table_title.shape[0])

table_addition = pd.DataFrame(add_details) 
table_addition.columns = [f'add_product_details_{f}' for f in range(table_addition.shape[1])]
table_addition.index = np.arange(0,table_addition.shape[0])

table_offers = pd.DataFrame(my_offer,columns=['offers'])
table_offers.index = np.arange(0,table_offers.shape[0])

table_cost   = pd.DataFrame(discounts,columns=['discount','cost'])
table_cost.index = np.arange(0,table_cost.shape[0])

final_table = pd.concat([table_title,table_p_details,table_addition,table_offers,table_cost],axis=1)

final_table.fillna("",inplace=True)

dummy =[]
for f,j in zip(final_table['offers'],final_table.index):
    count=0
    for k in f:
        if 'GST' in k:
            count+=1
            gst = k
            #print(k)
    if count==1:
        dummy.append(gst)
    if count==0:
        dummy.append('')


final_table['GST_details'] = dummy

# final_table.columns = ['Title','Brand','Model Name','Operating System','product_details_3', 'product_details_4', 'add_product_details_0',
#        'add_product_details_1', 'add_product_details_2',
#        'add_product_details_3', 'add_product_details_4',
#        'add_product_details_5', 'add_product_details_6',
#        'add_product_details_7', 'offers', 'discount', 'cost', 'GST_details']


final_table.to_excel(file_path,index=False)