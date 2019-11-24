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
PORT = 12305 # Arbitrary non-privileged port
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


def Amazon():
    
    links = []
    counter = 0
    html_page = urllib.request.urlopen(url_keyword)
    soup = BeautifulSoup(html_page)
    items = soup.findAll('a')
    for link in items[50:]:
        if (counter < 50):                           # counter determines how many products to look for in the wwebpage
            counter = counter + 1
            links.append(link.get('href'))           
        else:
            break

    #print (links)
    temp_str = ""
    asin_array=[] #array for asin numbers
    asin_array1=[]
    start = 'dp/B'
    end = "c"
    for url in links:
        try:
            temp_str = url[url.find(start)+3:url.find(start)+3+10]
            #print (temp_str)
            if (temp_str[0] == 'B'):
                asin_array1.append(temp_str)
        except AttributeError:

            continue

    asin_array = Remove(asin_array1)    # asin_array contains some product codes. These correspond to what is search in the variable keyword below. When
                                        # you run this code, some prodict codes are printed here like B03423405 etc. This is for Amazon
                                        # Similarly figure it out for walmart and target as to how product codes are stored and implement it. More than 3/4th of the
                                        # code is similar.
    print (asin_array)




    url_array=[] #array for urls


    all_items=[] #The final 2D list containing prices and details of products, that will be converted to a consumable csv
    x=0
    for asin in asin_array:
        if (x <4):
            item_array=[] #An array to store details of a single product.
            amazon_url="https://www.amazon.com/dp/"+asin #The general structure of a url            # find out how it is for walmart and target aswell. 
            response = requests.get(amazon_url, headers=headers, verify=False) #get the response


        #print (item_array)
            doc = html.fromstring(response.content)
           # print (doc.text())
            XPATH_NAME = '//h1[@id="title"]//text()'
       
            XPATH_ORIGINAL_PRICE = '//span[@class="a-size-medium a-color-price"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)

            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
           
            
        
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
          
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            #if ORIGINAL_PRICE == None:
            #    continue
            #print(ORIGINAL_PRICE[0:10])
     
            if response.status_code!=200:
                raise ValueError('captha')
            data = {
                    'NAME':NAME[0:40],
   
                    'ORIGINAL_PRICE':ORIGINAL_PRICE[0:10],
                    #'ORIGINAL_PRICE':ORIGINAL_PRICE,
              #      'AVAILABILITY':AVAILABILITY,
                    'URL':amazon_url,
                    }
            all_items.append(data)
            sleep(3)
            f=open('data.json','w')
            json.dump(all_items,f,indent=4)
            x=x+1
       # print(all_items)



# the below 3 lines of code were used for testing without an TCP connection.
keyword = "google+home+mini"   # product to look for 
url_keyword = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + keyword
Amazon()




## leave the below commented code commented itself. It is not required now.


'''

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
    url_keyword = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + keyword
    print(url_keyword)
    start_time = time.time()
    Amazon()
    end_time = time.time() - start_time
    print (end_time)
    print('Done')

    sleep(3)
    filename='data.json' #In the same folder or path is this file running must the file you want to tranfser to be
    f = open(filename,'rb')
    l = f.read(1024)
    #print(l)
    while (l):
       #sleep(3)
       conn.send(l)
       #print('Sent ',repr(l))
       l = f.read(1024)
      # print (l)
    f.close()

    print('Done sending')
    #break
    #conn.send('Thank you for connecting')
    #print(conn.recv(1024))
    #conn.send(all_items)
    



conn.close() # closing connection with the client
#s.close() # closing the socket
'''

