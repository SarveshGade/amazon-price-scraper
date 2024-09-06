from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from urllib.request import Request, urlopen
from time import sleep

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def search_product_list(interval_count = 1, interval_hours = 6):
    """
    This function searches for the price of a certain amazon product. This was intended to be part of a larger product to track
    how product prices changed over time, hence the input "interval_count", etc.

    """
    # prod_tracker = pd.read_csv('trackers/TRACKER_PRODUCTS.csv', sep=';')
    
    prod_tracker_URLS = input("Insert the url of the object: ")
    prod_buy_under = input("Alert when price is under...: ")
    tracker_log = pd.DataFrame()
    now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
    interval = 0 # counter reset
    
    while interval < interval_count:

        
            req = Request(prod_tracker_URLS, headers=HEADERS)
            page = urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            
            #product title
            title = soup.find(id='productTitle').get_text().strip()
            
            # to prevent script from crashing when there isn't a price for the product
            try:
                #price = float(soup.find(class_='a-price-whole').get_text().replace('.', '').replace('$', '').replace(',', '.').strip())
                price = soup.select_one("span.a-price span").get_text().replace('.', '').replace('$','').replace(',','').strip()
                price = price[:-2] + "." + price[-2:]
            except:
                # this part gets the price in dollars from amazon.com store
                try:
                    #price = float(soup.find(class_='a-price-whole').get_text().replace('$', '').replace(',', '').strip())
                    price = soup.select_one("span.a-price span").text
                    price = price[:-2] + "." + price[-2:]
                except:
                    price = ''

            try:
                review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-"]')[0].get_text().split(' ')[0].replace(",", "."))
                review_count = int(soup.select('#acrCustomerReviewText')[0].get_text().split(' ')[0].replace(".", ""))
            except:
                # sometimes review_score is in a different position... had to add this alternative with another try statement
                try:
                    review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-"]')[1].get_text().split(' ')[0].replace(",", "."))
                    review_count = int(soup.select('#acrCustomerReviewText')[0].get_text().split(' ')[0].replace(".", ""))
                except:
                    review_score = ''
                    review_count = ''
            
            # checking if there is "Out of stock"
            try:
                soup.select('#availability .a-color-state')[0].get_text().strip()
                stock = 'Out of Stock'
            except:
                # checking if there is "Out of stock" on a second possible position
                try:
                    soup.select('#availability .a-color-price')[0].get_text().strip()
                    stock = 'Out of Stock'
                except:
                    # if there is any error in the previous try statements, it means the product is available
                    stock = 'Available'
            """
            log = pd.DataFrame({'date': now.replace('h',':').replace('m',''),
                                #'code': prod_tracker.code[x], # this code comes from the TRACKER_PRODUCTS file
                                #'url': url,
                                'title': title,
                                'buy_below': prod_buy_under, # this price comes from the TRACKER_PRODUCTS file
                                'price': price,
                                'stock': stock,
                                'review_score': review_score,
                                'review_count': review_count})
            """
            try:
                # This is where you can integrate an email alert!
                if float(price) < prod_buy_under:
                    print('************************ ALERT! Buy the item ************************')
            
            except:
                # sometimes we don't get any price, so there will be an error in the if condition above
                pass

            # tracker_log = tracker_log.append(log)
            print('appended '+ '\n' + price + '\n\n')            
            sleep(5)
        
            interval += 1# counter update
        
            sleep(interval_hours*1*1)
            print('end of interval '+ str(interval))
    
    

search_product_list()
