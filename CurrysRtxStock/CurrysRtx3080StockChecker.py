from selenium import webdriver
from price_parser import parse_price
import asyncio
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from ProductModel import ProductModel 
from playsound import playsound
import time

#search strings for all cards and test.
web_page = 'https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/324_3091_30343_xx_xx/xx-criteria.html'
test_page = 'https://www.currys.co.uk/gbuk/household-appliances/laundry/washing-machines/332_3119_30206_xx_xx/xx-criteria.html'
#chromedriver path
executable_path = 'C:\\Users\cchen\Downloads\chromedriver_win32\chromedriver.exe'
#gets chromedriver
driver = webdriver.Chrome(executable_path)
#list product saved to 
products_list = []
#counter to check if page has already been loaded
counter_chrome = 0 
counter_refresh = 0

def open_chrome(): 
    driver.get(web_page)
    accept_cookie()   

def accept_cookie():
     driver.implicitly_wait(2)
     try:
         driver.find_element_by_id('onetrust-accept-btn-handler').click()
     except NoSuchElementException :
         print("button not found")
         accept_cookie()
   

def get_all_products():        
    elements_with_the_dynamic_id = driver.find_elements_by_css_selector('[id*="product10"]')
    
    for element in elements_with_the_dynamic_id:
        product_title = element.find_element_by_class_name('productTitle')
        product_price = element.find_element_by_class_name('productPrices')
        product_availability = element.find_element_by_class_name('channels-availability')        
        name = product_title.text   
        extracted_text = product_price.text.split("\n")
        unformatted_price = extracted_text[0]
        price = unformatted_price
        in_stock = product_availability.text  
        tag_with_link_to_product = element.find_element_by_tag_name('a')
        link_to_product = tag_with_link_to_product.get_attribute('href')        
        obj = ProductModel(name, price, in_stock, link_to_product)
        products_list.append(obj)

def check_when_in_stock():
     for product in products_list:
         if product.in_stock_for_delivery.startswith("Not"):
             print(product.name)
             print(product.price)
             print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------")
             print(product.link_to_product)
             print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------")
             print("still not in-stock\n")             
         elif product.in_stock_for_delivery.startswith("FREE"):
              print(product.name)
              print(product.price)
              print("in-stock, Credit Card to the ready tally ho")
              print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------")
              print(product.link_to_product)
              print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------")                        
              playsound('C:\\Users\cchen\Downloads\Siren.mp3')

print("counter refresh %s \n" % counter_refresh )  


def open_products_in_tabs():
    for product in products_list:
        driver.execute_script("window.open(%s,'_blank')", product.link_to_product)
        driver.get(product.link_to_product)
         
while True:

    if counter_chrome == 0:
        open_chrome()
        counter_chrome += 1
    else: 
        get_all_products()
        check_when_in_stock()
        open_products_in_tabs()
        time.sleep(5)       
        driver.refresh()
        counter_refresh += 1
