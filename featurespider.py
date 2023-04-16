import scrapy
# pageCount = 1
# class OlxSpider(scrapy.Spider):
    
    
       
#    # list = ['Brand', 'skoda', 'Model', 'Ad Type', 'Fuel Type', 'Price', 'Price Type', 'Payment Options', 'Year','Kilometers', 'Transmission Type', 'Used', 'Color','Body Type', 'Engine Capacity (CC)',  'Video', 'Virtual Tour']
#     name = 'feature'
#     start_urls = ['https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?filter=new_used_eq_2%2Cyear_between_2000_to_2023']
    
#     def parse(self, response):
           
#             global pageCount
#             # for url in response.css('div._41d2b9f3 a::attr(href)'):
#             #     yield response.follow(url.get(),callback = self.parsePage)
             
#             for listing in response.css('li.c46f3bfe'):
#                 url = listing.css('div._41d2b9f3 a::attr(href)').get()
#                 adDate = listing.css('span._2e28a695 span::text').get()
#                 if "hour" in adDate or "hours" in adDate or "day" in adDate or "days" in adDate or "week" in adDate or "weeks" in adDate or "1 month" in adDate:
#                      yield response.follow(url,callback = self.parsePage)
                      

#             pageCount = pageCount + 1
            
#             yield scrapy.Request(f'https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?page={pageCount}&filter=new_used_eq_2%2Cyear_between_2000_to_2023',callback=self.parse,)
          
#     def parsePage(self, response):
            
#             extraFeatures = response.css('div._27f9c8ac span::text').getall()

#             for feature in extraFeatures:
#                 yield{
#                     'ownerLink': response.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[2]/div/a').attrib['href'],
#                     'adID': response.css('div._171225da::text').get().replace('Ad id ', ''),
#                     'feature': feature
                 
#                 }
import scrapy
import csv

class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        with open('adID.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                value = row[0]
                link = f'https://www.olx.com.eg/en/ad/{value}'
                yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        try:
            extraFeatures = response.css('div._27f9c8ac span::text').getall()
        except: 
            extraFeatures = 'None'
            
        for feature in extraFeatures:
            yield{
               # 'ownerLink': response.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[2]/div/a').attrib['href'],
                'adID': response.css('div._171225da::text').get().replace('Ad id ', ''),
                'feature': feature

            }




