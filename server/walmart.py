import socket
import sys
from time import sleep
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
import csv
from requests_html import HTMLSession
import requests
import json
from lxml import html
import httplib2
import time
import datetime




def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 




HOST = "" # Symbolic name meaning all available interfaces
PORT = 12306 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
session = HTMLSession()   #declare a session object
#session = requests.Session() #python 2.7

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

'''
resp = urllib.request.urlopen("https://www.target.com/s?searchTerm=shampoo")
soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))

for link in soup.find_all('a', href=True):
    print(link['href'])

'''


def Walmart():
    links = []
    counter = 0
    # encoded_url = urlencode(url_keyword)
    # print(encoded_url)
    # print(encoded_url)
    html_page = urllib.request.urlopen(url_keyword)
    # html_page = urllib.request.urlopen( https://www.walmart.com/search/?query=google+home+mini)
    soup = BeautifulSoup(html_page)
   # print (soup)
    items = soup.findAll('a')

    for link in items[650:]:
        if (counter < 1000):                           # counter determines how many products to look for in the wwebpage
            counter = counter + 1
            links.append(link.get('href'))
        else:
            break

    #print(links)



    temp_str = ""
    asin_array=[]
    asin_temp_array=[]
    start = '/'
    end = " "

    for url in links:
        try:
            temp_str = url[url.rfind(start)+1:url.rfind(start)+10]
            #if(temp_str[2] == '/')
            asin_temp_array.append(temp_str)
        except AttributeError:
            continue
    new_asin_array = []
    asin_array = Remove(asin_temp_array)
    for x in asin_array:
        if (len(x) == 8 or len(x) == 9 and (x[-1] != '#' or x[-1] != '?') and ((x[0] <= 'a' and x[0] >='z') or (x[0] <= 'A' and x[0] >='Z')) ):
            new_asin_array.append(x)
    print(new_asin_array)

    url_array=[] #array for urls


    all_items=[] #The final 2D list containing prices and details of products, that will be converted to a consumable csv
    x=0
    for asin in new_asin_array:
        if (x<4):
            item_array=[] #An array to store details of a single product.
            walmart_url="https://www.walmart.com/ip/"+asin #The general structure of a url            # find out how it is for walmart and target aswell.
            response = requests.get(walmart_url, headers=headers, verify=False) #get the response

        #print (item_array)
            doc = html.fromstring(response.content)
            # print(doc)
           # print (doc.text())
            XPATH_NAME = '//h1[@class="prod-ProductTitle no-margin font-normal heading-a"]//text()'
            # print(XPATH_NAME)
            #XPATH_ORIGINAL_PRICE = '//span[@class="a-size-medium a-color-price"]//text()'
            XPATH_ORIGINAL_PRICE = '//span[@class="price display-inline-block arrange-fit price price--stylized"]//text()'
            # print (XPATH_ORIGINAL_PRICE)
            RAW_NAME = doc.xpath(XPATH_NAME)
            # print (RAW_NAME[0])
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)

            RAW_NAME1 = RAW_NAME[0]
            RAW_ORIGINAL_PRICE1 = RAW_ORIGINAL_PRICE[0:4]
            # print(RAW_ORIGINAL_PRICE)

            NAME = ' '.join(''.join(RAW_NAME1).split()) if RAW_NAME1 else None

            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE1).strip() if RAW_ORIGINAL_PRICE1 else None
            # print(ORIGINAL_PRICE)

            if response.status_code!=200:
                raise ValueError('captha')
            data = {
                    'NAME':NAME[0:40],

                    'ORIGINAL_PRICE':ORIGINAL_PRICE[0:10],
              #      'AVAILABILITY':AVAILABILITY,
                    'URL':walmart_url,
                    }
            all_items.append(data)
            sleep(3)
            f=open('data1.json','w')
            json.dump(all_items,f,indent=4)
            x=x+1



'''
# the below 3 lines of code were used for testing without an TCP connection.
keyword = "google+home+mini"   # product to look for 
url_keyword = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + keyword
Amazon()

'''


## leave the below commented code commented itself. It is not required now.




print ('Socket created')
try:
	s.bind((HOST, PORT))
except :
	print ('Bind failed. Error Code : ')
	sys.exit()
print ('Socket bind complete')
s.listen(10)
print ('Socket now listening')
while (1):
#wait to accept a connection - blocking call
    conn, addr = s.accept()
#display client information
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    data = str(conn.recv(1024))
    sleep(1)
    #keyword = 'SHAMPOO'
    keyword = data[2:-1]
    print(keyword)
    url_keyword = 'https://www.walmart.com/search/?query='+keyword
    print(url_keyword)
    start_time = datetime.datetime.now()

    Walmart()
    end_time = datetime.datetime.now() - start_time
    print (end_time.seconds)
    print('Done')

    sleep(3)
    filename='data1.json' #In the same folder or path is this file running must the file you want to tranfser to be
    f = open(filename,'rb')
    l = f.read(1024)
    #print(l)
    while (l):
       #sleep(3)
       conn.send(l)
       #print('Sent ',repr(l))
       l = f.read(1024)
       #print (l)
    f.close()

    print('Done sending')
    #break
    #conn.send('Thank you for connecting')
    #print(conn.recv(1024))
    #conn.send(all_items)
    



conn.close() # closing connection with the client
#s.close() # closing the socket


