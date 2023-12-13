# ----------------------------------------------------------------------------|
# Import all libraries here. Those libraries are using in the code
# ----------------------------------------------------------------------------|
import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.filterwarnings("ignore")   # Disable all notifications when load webdriver


# --------------------------------------------------------------------------------------------|
# Inside this function- declare all webdriver components. I am using here chrome webdriver.
# --------------------------------------------------------------------------------------------|
def driver_conn():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")      # Make the browser Headless. if you don't want to see the display on chrome just uncomment this
    chrome_options.add_argument("--log-level=3")    # Removes error/warning/info messages displayed on the console
    chrome_options.add_argument("--disable-infobars")  # Disable infobars ""Chrome is being controlled by automated test software"  Although is isn't supported by Chrome anymore
    chrome_options.add_argument("start-maximized")     # Make chrome window full screen
    chrome_options.add_argument('--disable-gpu')       # Disable gmaximizepu (not load pictures fully)
    # chrome_options.add_argument("--incognito")       # If you want to run browser as incognito mode then uncomment it
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-extensions")     # Will disable developer mode extensions
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")    # retrieve_block
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])    # retrieve_block
    chrome_options.add_experimental_option('useAutomationExtension', False)    # retrieve_block
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')    # retrieve_block
    chrome_options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')    # retrieve_block
    chrome_options.add_argument('--accept-encoding=gzip, deflate, br')    # retrieve_block
    chrome_options.add_argument('--accept-language=en-US,en;q=0.9')    # retrieve_block
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)   #we have disabled pictures (so no time is wasted in loading them)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # you don't have to download chromedriver it will be downloaded by itself and will be saved in cache
    return driver



# --------------------------------------------------------------------------------------------|
# Inside this function- Implement full code for scrap data every pages from that link.
# --------------------------------------------------------------------------------------------|
def get_data():
    all_data = []               # Save all data in this array.
    driver = driver_conn()      # Load chrome webdriver by that webdriver function.
    print('==================== Getting url ====================')
    url = "https://www.sreality.cz/en/search/for-sale/apartments/praha?page="   # This is the base url. Ate the end of this url will put page-number in the while loop.
    pag = 0         # Page set initial value 0
    while True:     # Start while loop
        pag += 1    # Page increase by 1
        print(">>>>>>>>>>>>>> Page: " + str(pag))   # Print page number
        driver.get(url + str(pag))                  # From here- Driver load link. That means: that url + page number
        time.sleep(2)                               # Time sleep- That means wait 2 Second after load the link.
        soup = BeautifulSoup(driver.page_source, 'lxml')    # Soup- After load that page, full source code go into this soup lxml format.

        # In the web page source code(soup)- at first I am finding a div which class is 'dir-property-list'.
        # Then in that div I am finding every property. So I saw div which class is "property". I set find_all method to target all properties in a page.
        # try and except method is using here to avoid error. At first code go to in try method, if not find then go to except method to return null.
        try:
            lis = soup.find('div', {'class': 'dir-property-list'}).find_all('div', {'class': 'property'})
        except:
            lis = ''
        print("Listing here: ", len(lis))
        if len(lis) < 1:        # If lis have less than 1 element then it break the while loop and stop the code. That means that will be last over page.
            break
        for li in lis:          # Here I set for loop- In lis has many properties in a page. So, by for loop it will go one by one property.
            link = ''           # Here are I declare all data points which I want to scrap and set initial value ''
            title = ''          # ||
            address = ''        # ||
            price = ''          # ||
            tags = ''           # ||
            try:
                link = "https://www.sreality.cz" + li.find('a', {'class': 'title'})['href']     # Here I am finding 'Link' data in the source code(soup)
            except:
                pass
            try:
                title = li.find('a', {'class': 'title'}).text.replace('\n', '').strip()         # Here I am finding 'Title' data in the source code(soup)
            except:
                pass
            try:
                address = li.find('span', {'class': 'locality'}).text.replace('\n', '').strip() # Here I am finding 'Address' data in the source code(soup)
            except:
                pass
            try:
                price = li.find('span', {'class': 'norm-price'}).text.replace('\n', '').strip() # Here I am finding 'Price' data in the source code(soup)
            except:
                pass
            try:
                des = li.find('span', {'class': 'labels'}).find_all('span', {'class': 'label'})
                tags = '\n'.join(d.get_text(separator=" ", strip=True) for d in des)            # Here I am finding all 'Tags' data in the source code(soup)
            except:
                pass
            data = {                    # ----> Here are I enter all data points in this 'data' dictionary.
                'Link': link,
                'Title': title,
                'Address': address,
                'Price': price,
                'Tags': tags,
            }
            # print(data)
            all_data.append(data)           # Add 'data' dictionary to 'all_data' array
            df = pd.DataFrame(all_data)     # Make those data in pandas dataframe. Here are pandas means pd
            df = df.rename_axis("Index")    # Make a header Index for counting
            df.to_csv('Sreality_Data.csv', encoding='utf-8-sig')    # Save the pandas dataframe to CSV file with utf-8 file format.
        df = pd.DataFrame(all_data)         # Same as above
        df = df.rename_axis("Index")        # Same as above
        df.to_csv('Sreality_Data.csv', encoding='utf-8-sig')    # Same as above
    print("Scraping finish successfully........")
    driver.close()      # Close the chrome webdriver when it finished scraping

# It is the main function calling method. I work whole code in get_data() function. So script start from here.
if __name__ == '__main__':
    get_data()