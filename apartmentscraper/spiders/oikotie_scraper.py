__author__ = 'larkki'

import time
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from selenium import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from apartmentscraper.items import ApartmentscraperItem

class OikotieSpider(BaseSpider):
    name = 'oikotie'
    allowed_domains = ['oikotie.fi']
    #allowed_domains = ['mininova.org']
    #start_urls = ['http://www.mininova.org/today']
    # lahti, 48 items per page
    #start_urls = ["http://asunnot.oikotie.fi/myytavat-asunnot#view=list&module=apartment-sell&offset=0&limit=2&sortby=published%20desc&aslocation%5Blocationids%5D%5B%5D=192%7C6%7C60.982994%7C25.65739%7CLahti&asprice%5Bsuffix%5D=000&asprice%5Bmin%5D=&asprice%5Bmax%5D=&assize%5Bmin%5D=30&assize%5Bmax%5D=60&assettings%5Bchanged%5D=1&assettings%5Bcollapsed%5D=1&asbuildyear%5Bmin%5D=&asbuildyear%5Bmax%5D=&assizelot%5Bmin%5D=&assizelot%5Bmax%5D=&asnewdevelopment%5Bnew_development%5D=1&aspublished%5Bpublished%5D=1"]
    start_urls = ["http://asunnot.oikotie.fi/myytavat-asunnot"]


    def parse(self, response):
        self.browser.get(response.url) # Load page

        searchbox = self.browser.find_element_by_id("magicbox")
        searchbox.send_keys("Lahti\r\n")
        #searchbox.send_keys(Keys.ENTER)
        time.sleep(1)
        size_min = self.browser.find_element_by_id("assize-min")
        size_min.send_keys("30")
        size_max = self.browser.find_element_by_id("assize-max")
        size_max.send_keys("60")
        pager = self.browser.find_element_by_xpath("//*[@id='sublist']/span[2]/span[2]")
        pager.click()
        pager48 = self.browser.find_element_by_xpath("//*[@id='sublist']/span[2]/span[3]/span[1]/span[3]")
        pager48.click()

        time.sleep(1)
        apartment_urls = []
        while True:
            urls = self.browser.find_elements_by_xpath("/html//div[@class='card card-ad']/div[@class='background']/div[@class='content']/div[@class='image']/a")
            for url in urls:
                link = url.get_attribute('href')
                apartment_urls.append(link)
                print(link)
            print("apartment_urls found %s" % len(apartment_urls))

            try:
                next_button_disabled = self.browser.find_element_by_xpath("//*[@id='search-view-list']/div[1]/div/div[1][@class='next disabled']")
                # we found the end of the list, exit the while loop
                break

            except:
                # advance to next page
                next_button = self.browser.find_element_by_xpath("//*[@id='search-view-list']/div[1]/div/div[1]")
                next_button.click()
                time.sleep(1)

        for url in apartment_urls:
            yield Request(url, callback=self.parse_apartment_info)


    def parse_apartment_info(self, response):
        self.browser.get(response.url) # Load page

        #Wait for javscript to load in Selenium
        time.sleep(1)

        xpaths = {
            "name": "/html/body[@id='apartment-sell-ad-index']/div[@id='outer-container']/div[@id='container']/div[@id='content']/div[@class='column-container']/div[@class='column']/div[@id='widget-ad-header']/div[@class='address-header']/h2/strong",
            "address": "//table//tr[th/text()[contains(.,'Sijainti')]]/td",
            "location": "//table//tr[th/text()[contains(.,'Kaupunginosa')]]/td",
            "surface_area": "//table//tr[th/text()[contains(.,'Asuinpinta-ala')]]/td",
            "price": "//table//tr[th/text()[contains(.,'Velaton myyntihinta')]]/td",
            "monthly_costs": "//table//tr[th/text()[contains(.,'Hoitovastike')]]/td",
            "construction_year": "//table//tr[th/text()[contains(.,'Rakennusvuosi')]]/td"}

        item = ApartmentscraperItem()
        item['url'] = response.url

        #loop the xpaths
        for k, v in xpaths.iteritems():
            try:
                item[k] = self.browser.find_element_by_xpath(v).text
            except NoSuchElementException:
                print "Couldn't find element"
            except:
                print "Something strange happened."

        return item


    def __init__(self):
        #CrawlSpider.__init__(self)
        self.verificationErrors = []
        self.browser = webdriver.Firefox()

        #self.selenium = selenium("localhost", 4444, "*chrome", "http://www.google.com")
        #self.selenium.start()

    def __del__(self):
        #self.selenium.stop()
        self.browser.close()
        print self.verificationErrors
        #CrawlSpider.__del__(self)
