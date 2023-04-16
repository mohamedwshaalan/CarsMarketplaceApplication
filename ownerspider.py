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

            # options = webdriver.ChromeOptions()
            # options.add_argument('headless')
            # driver = webdriver.Chrome(
            #     executable_path="./chromedriver", options=options)

            # driver.get(response)

            # for cookie in cookiesJson:
            #     driver.add_cookie(cookie)

            # driver.refresh()
            # # time.sleep(3)
            # # wait for page to load using explicit wait
            # wait = WebDriverWait(driver, 10)
            # button = driver.find_element(
            # By.CSS_SELECTOR, '#body-wrapper > div > header:nth-child(3) > div > div > div > div._0a9bc591 > div._408759e3 > div:nth-child(2) > div > div._1075545d.b34f9439._42f36e3b._96d4439a._1709dcb4 > span._09eb0c84._79855a31')

            # # click button
            # button.click()
            # try:
            #      ownerNumber = response.selector.xpath('//*[@id="body-wrapper"]/div/header[2]/div/div/div/div[4]/div[2]/div[2]/div/div[3]/span/text()').get()
            # except:
            #         ownerNumber = None
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
                #'ownerJoinDate': response.css(' div._05330198 span::text').get().replace('Member since ', ''),
                 'ownerJoinDate' : ownerJoinDate,
                #  'ownerNumber': ownerNumber
            }



