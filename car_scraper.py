from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

car_name=[] #List to store car name of the product
price=[] #List to store price of the product
miles=[] #List to store miles of the product
url_list=[] #List to store url of the product
pages=[] #List to store number of pages in search
years=[] #List to store car year

makes=[] #List to store the car make
make_checked=[] #List to store the car makes that are filtered for
models=[] #List to store the car model
model_checked=[] #List to store the car models that are filtered for

exterior_color=[] #List to store the exterior color of the car
interior_color=[] #List to store the inerior color of the car
transmissions=[] #List to store the transmission type
drivetrains=[] #List to store the drivetrain type
sellers=[] #List to store the name of the seller

makelist=[] #List to store all possible makes
makelist_title=[] #List that stores all possible makes with a title format
modellist=[] #List to store all possible models
modellist_title=[] #List that stores all possible makes with a title format

year_filter=[] #List that stores all possible years to filter by

options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(ChromeDriverManager().install(), options = options) # diver
driver.get('https://www.cars.com')
time.sleep(1)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Stores all of the possible makes
for a in soup.findAll('select', {'name' : 'makeId'}):
    for b in a.findAll('option'):
        makelist.append(str(b.text))
        makelist_title.append(str(b.text).title())

print("The list of makes are {}".format(makelist_title))
user_make = input('Please type a make from the list above:\n').title()
user_make = makelist[makelist_title.index(user_make)]
make_id = soup.find('option', text = user_make).get('value')
drpMake = Select(driver.find_element_by_name('makeId'))
drpMake.select_by_visible_text(user_make)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Stores all of the possible models for that specific make
for a in soup.findAll('select', {'name' : 'modelId'}):
    for b in a.findAll('option'):
        modellist.append(str(b.text))
        modellist_title.append(str(b.text).title().replace("- ",""))

print("The list of models are {}".format(modellist_title))
user_model = input('Please type a model from the list above:\n').title()
user_model = modellist[modellist_title.index(user_model)]
model_id = soup.find('option', text = user_model).get('value')
drpModel = Select(driver.find_element_by_name('modelId'))
drpModel.select_by_visible_text(user_model)

drpRange = Select(driver.find_element_by_name('radius'))
drpRange.select_by_visible_text('All Miles from')

zipcode = driver.find_element_by_name('zip')
zipcode.clear()
zipcode.send_keys('80011')

driver.find_element_by_class_name('NZE2g').click()
time.sleep(1)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Stores all possible years to filter by
for a in soup.findAll('select', {"name" : "yrId"}):
    for b in a.findAll('option'):
        if b.text not in year_filter:
            year_filter.append(str(b.text))


print("The list of possible years to filter by are {}".format(year_filter))
user_min_year = input('Please select a minimum year from the list above:\n').title()
user_max_year = input('Please select a maximum year from the list above:\n').title()
min_year_id = soup.find('option', text = user_min_year).get('value')
max_year_id = soup.find('option', text = user_max_year).get('value')
drpYearMin = Select(driver.find_element_by_xpath('//*[@id="yearRange"]/div[3]/div/div[1]/div/select'))
drpYearMin.select_by_visible_text(user_min_year)
drpYearMax = Select(driver.find_element_by_xpath('//*[@id="yearRange"]/div[3]/div/div[3]/div/select'))
drpYearMax.select_by_visible_text(user_max_year)

time.sleep(1)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Used to store the page numbers in a list
for a in soup.findAll('ul', class_ = "page-list"):
    for b in a.findAll('a'):
        page = str(b.get('data-page'))
        pages.append(page)

# Scrolls thru all pages and stores the information
for pg in pages:
    dev_url = 'https://www.cars.com/for-sale/searchresults.action/?mdId=' + model_id + '&mkId=' + make_id + '&page=' + pg + '&perPage=20&rd=99999&searchSource=PAGINATION&sort=relevance&yrId=' + min_year_id + '%2C' + max_year_id + '&zc=80011'
    driver.get(dev_url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Used to populate the lists
    for a in soup.findAll(class_ = "shop-srp-listings__listing-container"):
        # Used to see if that listing has a name otherwise store it as N/A
        if('\"listing-row__title\"' in str(a)):
            name = str(a.find('h2', class_ = 'listing-row__title').text).strip()
        else:
            name = 'N/A'

        if name != 'N/A':
            year = name[:4]
            name = name[5:]
        else:
            year = 'N/A'

        years.append(year)
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
        if('\"shop-srp-listings__listing\"' in str(a)):
            link = 'cars.com' + a.find('a', class_ = 'shop-srp-listings__listing').get('href')
        else:
            link = 'N/A'
        url_list.append(link)


        # Used to store the meta data
        if('\"listing-row__meta\"' in str(a)):
            meta_data = str(a.find('ul', class_ = "listing-row__meta").text).strip()
            ext_clr = meta_data.replace("  ","").splitlines()[2]
            int_clr = meta_data.replace("  ","").splitlines()[7]
            transmission = meta_data.replace("  ","").splitlines()[12]
            drivetrain = meta_data.replace("  ","").splitlines()[17]
        exterior_color.append(ext_clr)
        interior_color.append(int_clr)
        transmissions.append(transmission)
        drivetrains.append(drivetrain)


        # Used to store the seller otherwise store it as N/A
        if('\"dealer-name\"' in str(a)):
            seller = str(a.find('div', class_ = 'dealer-name').text).strip().splitlines()[0]
        else:
            seller = 'N/A'
        sellers.append(seller)

for a in soup.findAll('li', class_ = "checkbox shortlist"):
    if('\"checked\"' in str(a)):
        if(str(a.find('input', class_ = "checkbox__input").get("data-dimensionlabel")).lower() == 'make'):
            make = str(a.find('label', class_ = "checkbox__label").text).strip()
            make_checked.append(make)
        if(str(a.find('input', class_ = "checkbox__input").get("data-dimensionlabel")).lower() == 'model'):
            model = str(a.find('label', class_ = "checkbox__label").text).strip()
            model_checked.append(model)

for car in car_name:
    for make in make_checked:
        if(make in car):
            makes.append(make)

for car in car_name:
    for model in model_checked:
        if(model in car):
            models.append(model)


df = pd.DataFrame({'Car Name':car_name,'Year':years,'Make':makes,'Model':models,\
'Price':price,'Mileage':miles,'Exterior Color':exterior_color,'Interior Color':interior_color,\
'Transmission':transmissions,'Drivetrain':drivetrains,'Seller':sellers,'Link':url_list})

df.to_csv('car_data.csv', index=False, encoding='utf-8')
