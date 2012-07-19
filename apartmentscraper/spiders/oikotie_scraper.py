__author__ = 'larkki'

import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from selenium import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from apartmentscraper.items import ApartmentscraperItem

class OikotieSpider(CrawlSpider):
    name = 'oikotie'
    allowed_domains = ['oikotie.fi']
    #allowed_domains = ['mininova.org']
    #start_urls = ['http://www.mininova.org/today']
    # lahti, 48 items per page
    #start_urls = ['http://asunnot.oikotie.fi/myytavat-asunnot#view=list&module=apartment-sell&offset=0&limit=2&sortby=published%20desc&aslocation%5Blocationids%5D%5B%5D=192%7C6%7C60.982994%7C25.65739%7CLahti&asprice%5Bsuffix%5D=000&asprice%5Bmin%5D=&asprice%5Bmax%5D=&assize%5Bmin%5D=30&assize%5Bmax%5D=60&assettings%5Bchanged%5D=1&assettings%5Bcollapsed%5D=1&asbuildyear%5Bmin%5D=&asbuildyear%5Bmax%5D=&assizelot%5Bmin%5D=&assizelot%5Bmax%5D=&asnewdevelopment%5Bnew_development%5D=1&aspublished%5Bpublished%5D=1']
    start_urls = ['http://asunnot.oikotie.fi/myytavat-asunnot']
    rules = ([Rule(SgmlLinkExtractor(allow=['/myytavat-asunnot/\d+']), 'parse_page', follow=True)])


    def parse_page(self, response):

        #sel = self.selenium
        #sel.open(response.url)
        self.browser.get(response.url) # Load page

        #Wait for javscript to load in Selenium
        time.sleep(2.5)

        #Do some crawling of javascript created content with Selenium

        #hxs = HtmlXPathSelector(response)
        #item['name'] = hxs.select("//h1/text()").extract()
        #item['name'] = sel.get_text("//h1/text()")

        item = ApartmentscraperItem()
        item['url'] = response.url
        item['name'] = self.browser.find_element_by_xpath("//h1").text
        item['location'] = self.browser.find_element_by_xpath("/html/body[@id='apartment-sell-ad-index']/div[@id='outer-container']/div[@id='container']/div[@id='content']/div[@class='column-container']/div[@class='column-wrapper two-thirds']/div[@class='column']/div[@id='widget-ad-information']/div[@class='box']/div[@class='widget-ad-information-table']/table/tbody/tr[1]/td").text
        item['surface_area'] = self.browser.find_element_by_xpath("/html/body[@id='apartment-sell-ad-index']/div[@id='outer-container']/div[@id='container']/div[@id='content']/div[@class='column-container']/div[@class='column-wrapper two-thirds']/div[@class='column']/div[@id='widget-ad-information']/div[@class='box']/div[@class='widget-ad-information-table']/table/tbody/tr[4]/td").text
        item['price'] = self.browser.find_element_by_xpath("/html/body[@id='apartment-sell-ad-index']/div[@id='outer-container']/div[@id='container']/div[@id='content']/div[@class='column-container']/div[@class='column-wrapper two-thirds']/div[@class='column']/div[@id='widget-ad-information']/div[@class='box box-1']/div[@class='widget-ad-information-table']/table/tbody/tr[1]/td").text
        item['montly_expenses'] = self.browser.find_element_by_xpath("/html/body[@id='apartment-sell-ad-index']/div[@id='outer-container']/div[@id='container']/div[@id='content']/div[@class='column-container']/div[@class='column-wrapper two-thirds']/div[@class='column']/div[@id='widget-ad-information']/div[@class='box box-1']/div[@class='widget-ad-information-table']/table/tbody/tr[5]/td").text
        item['construction_year'] = self.browser.find_element_by_xpath("/html/body[@id='apartment-sell-ad-index']/div[@id='outer-container']/div[@id='container']/div[@id='content']/div[@class='column-container']/div[@class='column-wrapper two-thirds']/div[@class='column']/div[@id='widget-ad-information-building']/div[@class='box box-1']/div[@class='widget-ad-information-table']/table/tbody/tr[4]/td").text

        #filename = response.url
        #open(filename, 'wb').write(response.body)

        return item


    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        self.browser = webdriver.Firefox()

        #self.selenium = selenium("localhost", 4444, "*chrome", "http://www.google.com")
        #self.selenium.start()

    def __del__(self):
        #self.selenium.stop()
        self.browser.close()
        print self.verificationErrors
        CrawlSpider.__del__(self)
