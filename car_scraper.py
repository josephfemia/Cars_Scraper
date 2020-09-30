from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install()) # diver

car_name=[] #List to store car name of the product
price=[] #List to store price of the product
miles=[] #List to store miles of the product
url=[] #List to store url of the product
driver.get("https://www.cars.com/for-sale/searchresults.action/?mdId=36302758&mkId=20014&rd=99999&searchSource=QUICK_FORM&zc=80011")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
#print(soup.prettify())

# print(soup.findAll('h2', class_="listing-row__title"))
# print(soup.findAll('span', class_="listing-row__mileage"))
# print(soup.findAll('span', class_="listing-row__price"))
print(soup.find(class_ = "shop-srp-listings__listing"))


# for a in soup.findAll('h2', class_='listing-row__title'):
#     name = str(a.text)
    # price=a.find('div', attrs={'class':'snapshot__body-content snapshot__details-price'})
    # rating=a.find('div', attrs={'class':'snapshot__details-miles item-value'})
    # products.append(name.text)
    # prices.append(price.text)
    # ratings.append(rating.text)
    # print(name)
    # print(price)
    # print(rating)

# df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})
# df.to_csv('products.csv', index=False, encoding='utf-8')
