import time
from bs4 import BeautifulSoup as bs
from PIL import Image
import requests
from selenium import webdriver
import scrapy
import os
import io

class scraper(scrapy.Spider):
    def __init__ (self):
        self.base_url = ""
        self.driver = webdriver.Chrome("")
        # Directory to save the scraping results
        self.dDirectory = ""
        # Links to visit
        self.to_visit = dict()
        # Specific for ASOS
    def getLinks(self):
        for i in range(1,2):
            url = self.base_url+str(i)
            self.to_visit[url] = ""
        return self.to_visit
    def getContent(self):
        for link in self.to_visit.keys():
            self.driver.get(link)
            self.to_visit[link] = self.driver.page_source
            time.sleep(3)
    def downloadImages(self):
        for link in self.to_visit.keys():
            try:
                for img in bs(self.to_visit[link],features="lxml").findAll("img",{'data-auto-id':'productTileImage'}):
                    img_href = img["src"]
                    img_name = img['alt']
                    request = requests.get("https:"+img_href,timeout = 10).content
                    imageFile = io.BytesIO(request)
                    image = Image.open(imageFile).convert('RGB')
                    path = os.path.join(self.dDirectory+'/'+img_name+'.jpg')
                    with open(path,'wb') as f:
                        image.save(f,'JPEG')
                    print(img_name+" succesfully Downloaded")
            except:
                print("An exeption occured")





ins = scraper()
getLinks = ins.getLinks()
getContent = ins.getContent()
ins.downloadImages().head()