
import os 
import requests
import io
from PIL import Image
import pandas as pd
from selenium import webdriver
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
 
# print("Enter your folder location:reference format")
# print(r'"C:\Users\91883\Desktop\image_storage"')
# store_loc = input()

folder_path = os.path.join(os.getcwd(),'web_scrapping_projects','medical_application','output_file')
if not os.path.exists(os.path.join(folder_path,'csv_folder')):
    os.mkdir(os.path.join(folder_path,'csv_folder'))
    print("Folder csv created")

if not os.path.exists(os.path.join(folder_path,'img_folder')):
    os.mkdir(os.path.join(folder_path,'img_folder'))
    print("Folder Image created")

# if not os.path.exists(os.path.join(r"{}".format(store_loc[1:-1]),'csv_folder')):
#     os.mkdir(os.path.join(r"{}".format(store_loc[1:-1]),'csv_folder'))
#     print("Folder csv created")
# if not os.path.exists(os.path.join(r"{}".format(store_loc[1:-1]),'img_folder')):
#     os.mkdir(os.path.join(r"{}".format(store_loc[1:-1]),'img_folder'))
#     print("Folder Image created")

#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://dermnetnz.org/image-library')
driver.maximize_window()

img_downlod_url = driver.find_elements(by=By.XPATH,value='//div[@class="imageList__group__item__image"]/img')

dieases_name = driver.find_elements(by=By.XPATH,value='//div[@class="imageList__group__item__copy"]')

url = driver.find_elements(by=By.XPATH,value='//a[@class="imageList__group__item"]')

common_details = []
for sub_img_downlod_url,sub_dieases_name,sub_url in zip(img_downlod_url,dieases_name,url):
    common_details.append([sub_img_downlod_url.get_attribute('src'),sub_dieases_name.text,sub_url.get_attribute('href')])
    
img_download_,diseases_,url_ = zip(*common_details)
 
myexcel = pd.DataFrame(common_details,columns=['image_url','diseases_name','website_link'])

myexcel['search_letter'] = myexcel['diseases_name'].apply(lambda x: str(x)[0])

#myexcel.to_excel(os.path.join(r"{}".format(store_loc[1:-1]),'csv_folder','output.xlsx'),index=False)
#print("Csv File is generated created,'\n")
#myexcel.to_csv(os.path.join(r"{}".format(store_loc[1:-1]),'csv_folder','output.csv'),index=False)

myexcel.to_excel(os.path.join(folder_path,'csv_folder','output.xlsx'),index=False)
myexcel.to_csv(os.path.join(folder_path,'csv_folder','output.csv'),index=False)
print("Csv File is generated created,'\n")

for image_urls,name in zip(img_download_,diseases_):
    try:
        image_files = requests.get(image_urls).content
        images_file = io.BytesIO(image_files)
        image = Image.open(images_file)
        image.save(os.path.join(folder_path,'img_folder',f'{name}.png'))
        print(image_urls,'stored in image_folder','\n')
        break
    except:
           pass
    #break

