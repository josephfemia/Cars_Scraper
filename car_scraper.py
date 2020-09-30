from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

car_name=[] #List to store car name of the product
price=[] #List to store price of the product
miles=[] #List to store miles of the product
url_list=[] #List to store url of the product
pages=[] #List to store number of pages in search

# Test Url: https://www.cars.com/for-sale/searchresults.action/?mdId=36302758&mkId=20014&page=1&perPage=20&rd=99999&searchSource=PAGINATION&sort=relevance&zc=80011
# url = input('Please enter the link you would like to scrape:\n')
url = 'https://www.cars.com/for-sale/searchresults.action/?mdId=36302758&mkId=20014&page=1&perPage=20&rd=99999&searchSource=PAGINATION&sort=relevance&zc=80011'
driver = webdriver.Chrome(ChromeDriverManager().install()) # diver
driver.get(url)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')


# Used to store the page numbers in a list
for a in soup.findAll('ul', class_ = "page-list"):
    for b in a.findAll('a'):
        page = b.get('data-page')
        pages.append(page)

# Scrolls thru all pages and stores the information
for pg in pages:
    driver.get(url.replace("page=1", "page=" + pg))
    time.sleep(1)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Used to populate the lists
    for a in soup.findAll(class_ = "shop-srp-listings__listing-container"):
        # Used to see if that listing has a name otherwise store it as N/A
        if('\"listing-row__title\"' in str(a)):
            name = str(a.find('h2', class_ = 'listing-row__title').text).strip()
        else:
            name = 'N/A'
        car_name.append(name)


        # Used to see if that listing has a mileage listed otherwise store it as N/A
        if('\"listing-row__mileage\"' in str(a)):
            mi = str(a.find('span', class_ = 'listing-row__mileage').text).strip().replace('.', '')
        else:
            mi = 'N/A'
        miles.append(mi)


        # Used to see if that listing has a price listed otherwise store it as N/A
        if('\"listing-row__price\"' in str(a)):
            cost = str(a.find('span', class_ = 'listing-row__price').text).strip()
            if cost == 'Not Priced':
                cost = 'N/A'
        else:
            cost = 'N/A'
        price.append(cost)


        # Used to see if that listing has a url otherwise store it as N/A
        if('\"listing-row__price\"' in str(a)):
            link = 'cars.com' + a.find('a', class_ = 'shop-srp-listings__listing').get('href')
        else:
            link = 'N/A'
        url_list.append(link)

df = pd.DataFrame({'Car Name':car_name,'Price':price,'Mileage':miles, 'Link':url})
df.to_csv('car_data.csv', index=False, encoding='utf-8')
