import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from apartmentscraper.items import ApartmentscraperItem

from selenium import selenium

class SeleniumSpider(CrawlSpider):
    name = "HsSpider"
    start_urls = ["http://www.google.com"]
    #allowed_domains = ['google.com']

    rules = (
    Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page',follow=True),
    )

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://www.google.com")
        self.selenium.start()

    def __del__(self):
        self.selenium.stop()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse_page(self, response):


        hxs = HtmlXPathSelector(response)
        #Do some XPath selection with Scrapy
        hxs.select('//div').extract()

        sel = self.selenium
        sel.open(response.url)

        #Wait for javscript to load in Selenium
        if sel:
            time.sleep(2.5)

        #Do some crawling of javascript created content with Selenium
        sel.get_text("//div")

        item = ApartmentscraperItem()
        item['url'] = response.url
        item['name'] = hxs.select('//*[@id="gbqfsa"]').extract()
        item['location'] = hxs.select('//*[@id="portfolio"]/div[1]/h2').extract()

        return item