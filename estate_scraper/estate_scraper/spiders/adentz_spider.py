import re
import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod
from estate_scraper.items import EstateScraperItem

class RespiderSpider(scrapy.Spider):
    name = "adentz_spider"

    def start_requests(self):
        # Initial request to the website with Playwright support
        yield scrapy.Request('https://www.adentz.de/wohnung-mieten-rostock/#/list1',
                             meta={'playwright': True, 'playwright_page_methods': [
                                 # Accept cookies if prompted
                                 PageMethod('click', selector='//div[@class="col-md-6 col-12"]//a[@class="_brlbs-btn _brlbs-btn-accept-all _brlbs-cursor"]'),
                                 # Wait for the list of estates to be visible
                                 PageMethod('wait_for_selector', '//div[@class="hm_listbox"]/a')
                             ]})

    def parse(self, response):
        # Iterate over each estate link found on the page
        for estate in (
                response.xpath('//a[contains(@href, "javascript:IwAG.HomepageModul.getInstance().ToExpose")]/@href')
        ):
            href = estate.get()
            # Extract the unique identifier for the estate
            uuid = re.search(r'ToExpose\("([^"]+)"\)', href).group(1)
            # Construct the URL for the detailed estate page
            link = 'https://www.adentz.de/wohnung-mieten-rostock/#/expose' + uuid
            request = Request(url=link, callback=self.parse_page, meta={'playwright': True,
                                   'playwright_page_methods': [
                                   # Wait for the estate images to be visible
                                   PageMethod('wait_for_selector', '//div[@class="hm_image"]/a')
                                   ]}, dont_filter=True)
            yield request

    def parse_page(self, response):
        item = EstateScraperItem()
        item['url'] = response.request.url
        item['title'] = response.xpath('//*[@id="iwWidget"]/h1/text()').get().strip()
        item['status'] = 'no data'  # Placeholder for status, if needed later
        # Get all image URLs for the estate
        item['pictures'] = response.xpath('//div[@class="hm_image"]/a/img/@src').getall()
        raw_rent_price = response.xpath('//*[@id="iwWidget"]/span[1]/text()').get()
        # Extract the numerical part of the rent price
        rent_price = re.search(r'[\d.,]+', raw_rent_price)
        item['rent_price'] = rent_price.group().replace('.', '')
        # Extract and join all description texts
        description_texts = response.xpath('//*[@id="exposeview"]/div[4]').xpath('.//text()').getall()
        item['description'] = ' '.join([text.strip() for text in description_texts if text.strip()])
        # Extract the phone number
        raw_phone_number = response.xpath('//text()[contains(., "Mobil: ")]').get()
        item['phone_number'] = ''.join(re.findall(r'\d+', raw_phone_number))
        # Extract the email address
        item['email'] = response.xpath('//section[@class="av_textblock_section "]//text()[contains(., ".de")]').get()
        yield item
