import scrapy
import datetime
from datetime import datetime, timedelta
import json

with open('cookies.txt','r') as f:
    cookiesJson = json.load(f)

pageCount = 1
class OlxSpider(scrapy.Spider):
    
  
    name = 'owner'
    start_urls = ['https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?filter=new_used_eq_2%2Cyear_between_2000_to_2023']

    def parse(self, response):
           
            global pageCount
          
         
            for url in response.css('div._41d2b9f3 a::attr(href)'):
                yield response.follow(url.get(),callback = self.parsePage)

            pageCount = pageCount + 1
            yield scrapy.Request(f'https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?page={pageCount}&filter=new_used_eq_2%2Cyear_between_2000_to_2023',callback=self.parse,cookies=cookiesJson)
          
    def parsePage(self, response):

            try:
                  
                ownerJoinDate = response.css(' div._05330198 span::text').get().replace('Member since ', '')
                ownerJoinDate = ownerJoinDate.replace(' ', '-')
                ownerJoinDate = datetime.strptime(ownerJoinDate, '%b-%Y')
                ownerJoinDate = ownerJoinDate.strftime('%Y-%m-%d')
            except: 
                ownerJoinDate = None


            yield{

                'ownerLink': response.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[2]/div/a').attrib['href'],
                'ownerName': response.css('div._1075545d._6caa7349._42f36e3b.d059c029 span::text').get(),
                 'ownerJoinDate' : ownerJoinDate,
            }



