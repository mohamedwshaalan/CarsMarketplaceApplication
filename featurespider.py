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
                'adID': response.css('div._171225da::text').get().replace('Ad id ', ''),
                'feature': feature

            }




