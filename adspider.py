import scrapy
import re
import json
from scrapy.http import HtmlResponse
from scrapy import Request
import re
import datetime
from datetime import datetime, timedelta
pageCount = 1

class OlxSpider(scrapy.Spider):
    
    
       
   
    allowed_domains = ["www.olx.com.eg"]
    start_urls = ['https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?filter=new_used_eq_2%2Cyear_between_2000_to_2023']
    
    def parse(self, response):
           
            global pageCount
      

            
            with open('cookies.txt','r') as f:
                 cookiesJson = json.load(f)

            for listing in response.css('li.c46f3bfe'):
                adUrl = listing.css('div._41d2b9f3 a::attr(href)').get()
                adUrl = "https://www.olx.com.eg" + adUrl
                adDate = listing.css('span._2e28a695 span::text').get()
                if "hour" in adDate or "hours" in adDate or "day" in adDate or "days" in adDate or "week" in adDate or "weeks" in adDate or "1 month" in adDate:
                     request = Request(url=adUrl, cookies = cookiesJson, callback = self.parsePage)
                     request.cb_kwargs['isURL'] = True
                     yield request
                   
                      

            pageCount = pageCount + 1
            
            yield scrapy.Request(f'https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?page={pageCount}&filter=new_used_eq_2%2Cyear_between_2000_to_2023',callback=self.parse,cookies=cookiesJson)
          
    def parsePage(self,response: HtmlResponse, isURL: bool, **kwargs):
            
            if isURL:
                with open('cookies.txt','r') as f:
                    cookiesJson = json.load(f)
                detailsList = response.css('div.b44ca0b3 span::text').getall()

                detailTitles = detailsList[0::2]
                detailValues = detailsList[1::2]
                
                detailsDictionary = dict(zip(detailTitles, detailValues))

                carDetails = {}

                carDetails['Brand'] = detailsDictionary.get('Brand', None)
                carDetails['Model'] = detailsDictionary.get('Model', None)
                carDetails['Fuel Type'] = detailsDictionary.get('Fuel Type', None)
                carDetails['Price'] = detailsDictionary.get('Price', None)
                carDetails['Price Type'] = detailsDictionary.get('Price Type', None)
                carDetails['Payment Options'] = detailsDictionary.get('Payment Options', None)
                carDetails['Year'] = detailsDictionary.get('Year', None)
                carDetails['Transmission Type'] = detailsDictionary.get('Transmission Type', None)
                carDetails['Condition'] = detailsDictionary.get('Condition', None)
                carDetails['Color'] = detailsDictionary.get('Color', None)
                carDetails['Engine Capacity (CC)'] = detailsDictionary.get('Engine Capacity (CC)', None)
                carDetails['Kilometers'] = detailsDictionary.get('Kilometers', None)
                adId = response.selector.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[6]/div[1]/text()').get().replace('Ad id ', ''),
                apiUrl = f'https://www.olx.com.eg/api/listing/{adId[0]}/contactInfo/'
                
                
                     
                try: 
                    description = response.css('div._0f86855a span::text').get()
                except:

                    description = None
                
                try:
                    location = response.css('div._1075545d.e3cecb8b._5f872d11')
                    location = location.css('span::text').get().replace(', Cairo','')
                except:
                    location = None

                if carDetails['Engine Capacity (CC)'] != None:
                    engineCapacity = carDetails['Engine Capacity (CC)']

                    if "More than" in engineCapacity:
                        minimumCapacity = "3000"
                        maximumCapacity = "4000"
                    elif " - " in engineCapacity:
                        minimumCapacity = engineCapacity.split(" - ")[0]
                        maximumCapacity = engineCapacity.split(" - ")[1]
                    else:
                        minimumCapacity = engineCapacity
                        maximumCapacity = engineCapacity
                else:
                    minimumCapacity = None
                    maximumCapacity = None

                if carDetails['Kilometers'] != None:
                    kilometers = carDetails['Kilometers']

                    if "More than" in kilometers:
                        minimumKilometers = "200000"
                        maximumKilometers = "300000" 
                    else: 
                        minimumKilometers = kilometers.split(" to ")[0]
                        maximumKilometers = kilometers.split(" to ")[1]
                else:
                    minimumKilometers = None
                    maximumKilometers = None
                try: 
                    ownerJoinDate = response.css(' div._05330198 span::text').get().replace('Member since ', '')
                    ownerJoinDate = ownerJoinDate.replace(' ', '-')
                    ownerJoinDate = datetime.strptime(ownerJoinDate, '%b-%Y')
                    ownerJoinDate = ownerJoinDate.strftime('%Y-%m-%d')
                except: 
                    ownerJoinDate = None
                try:
                    extraFeatures = response.css('div._27f9c8ac span::text')
                    extraFeatures = extraFeatures.getall()
                    extraFeatures = ', '.join(extraFeatures)
                except:
                    extraFeatures = None
            
                extraPhoneNumbers = []
                if description != None:
                    phoneRegex = re.compile(r'01[0-9]{9}')
                    for match in phoneRegex.finditer(description):
                        extraPhoneNumbers.append(match.group())
                    if len(extraPhoneNumbers) == 1:
                        extraPhoneNumbers[0] = '0' + extraPhoneNumbers[0]
                    extraPhoneNumbers = ', '.join(extraPhoneNumbers)

                request = Request(url=apiUrl,cookies=cookiesJson,callback=self.parsePage)
                request.cb_kwargs['isURL'] = False
                request.cb_kwargs['info'] = {
                    'ownerLink': response.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[2]/div/a').attrib['href'],
                    'ownerJoinDate' : ownerJoinDate,
                    'ownerName': response.css('div._1075545d._6caa7349._42f36e3b.d059c029 span::text').get(),
                    'adID': adId,
                    'location': location,
                    'brand': carDetails['Brand'],
                    'model': carDetails['Model'],
                    'fuelType': carDetails['Fuel Type'], 
                    'price': carDetails['Price'],
                    'priceType': carDetails['Price Type'],
                    'paymentOption': carDetails['Payment Options'],
                    'year': carDetails['Year'],
                    'transmissionType': carDetails['Transmission Type'],
                    'condition': carDetails['Condition'],
                    'color': carDetails['Color'],
                    'minimumCapacity': minimumCapacity,
                    'maximumCapacity': maximumCapacity,
                    'minimumKilometers': minimumKilometers,
                    'maximumKilometers': maximumKilometers,
                    'extraFeatures': extraFeatures,
                    'description': description,
                    'extraPhoneNumbers': extraPhoneNumbers
                    
                }
                yield request
        
            else:
                englishRegex = re.compile(r'(\+?\d{1,3}[-\.\s]?)?\d{10,13}')
        
                numbers = []
                for match in englishRegex.finditer(response.text):
                    numbers.append(match.group(0))
                newInfo = {
                    'ownerLink': response.cb_kwargs['info']['ownerLink'],
                    'ownerJoinDate' : response.cb_kwargs['info']['ownerJoinDate'],
                    'ownerName': response.cb_kwargs['info']['ownerName'],
                    'adID': response.cb_kwargs['info']['adID'],
                    'location': response.cb_kwargs['info']['location'],
                    'brand': response.cb_kwargs['info']['brand'],
                    'model': response.cb_kwargs['info']['model'],
                    'fuelType': response.cb_kwargs['info']['fuelType'],
                    'price': response.cb_kwargs['info']['price'],
                    'priceType': response.cb_kwargs['info']['priceType'],
                    'paymentOption': response.cb_kwargs['info']['paymentOption'],
                    'year': response.cb_kwargs['info']['year'],
                    'transmissionType': response.cb_kwargs['info']['transmissionType'],
                    'condition': response.cb_kwargs['info']['condition'],
                    'color': response.cb_kwargs['info']['color'],
                    'minimumCapacity': response.cb_kwargs['info']['minimumCapacity'],
                    'maximumCapacity': response.cb_kwargs['info']['maximumCapacity'],
                    'minimumKilometers': response.cb_kwargs['info']['minimumKilometers'],
                    'maximumKilometers': response.cb_kwargs['info']['maximumKilometers'],
                    'extraFeatures': response.cb_kwargs['info']['extraFeatures'],
                    'description': response.cb_kwargs['info']['description'],
                    'extraPhoneNumbers': response.cb_kwargs['info']['extraPhoneNumbers'],
                    'phoneNumber': numbers[0],

                }
                if numbers[0] is not None:
                    yield newInfo

       


