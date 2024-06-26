import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod
from estate_scraper.items import EstateScraperItem


class RespiderSpider(scrapy.Spider):
    name = "respider"

    def start_requests(self):
        # Start request to a specific page with Playwright support
        yield scrapy.Request('https://kelm-immobilien.de/immobilien/page/999',
                             meta={'playwright': True})

    def parse(self, response):
        # Loop through each estate link found on the page
        for estate in response.css('h3.property-title a'):
            link = estate.css('::attr(href)').get()
            # Request to parse each estate's details with Playwright
            request = Request(url=link, callback=self.parse_page, meta={'playwright': True,
                                   'playwright_page_methods': [
                                   # Wait for images to load
                                   PageMethod('wait_for_selector', 'div.galleria-image img')
                                   ]})
            yield request

    def parse_page(self, response):
        item = EstateScraperItem()
        item['url'] = response.request.url
        item['title'] = response.xpath('//h1[@class="property-title"]/text()').get()
        # Extract status of the estate, defaulting to 'no data' if not found
        if response.xpath('//li[@class="list-group-item data-vermietet"]//div[@class="dt col-sm-5"]/text()').get() == 'Status':
            item['status'] = response.xpath('//li[@class="list-group-item data-vermietet"]//div[@class="dd col-sm-7"]/text()').get()
        else:
            item['status'] = 'no data'
        # Extract all image URLs for the estate
        item['pictures'] = response.xpath('//div[@class="galleria-image"]/img/@src').getall()
        # Extract the base rent price, handling 'only purchase' case
        if response.xpath('//li[@class="list-group-item data-kaltmiete"]//div[@class="dt col-sm-5"]/text()').get():
            item['rent_price'] = response.xpath('//li[@class="list-group-item data-kaltmiete"]//div[@class="dd col-sm-7"]/text()').get()[:-8].replace('.','')
        else:
            item['rent_price'] = 'only purchase'
        # Extract and clean the description text of the estate
        description_div = response.xpath('//div[@class="property-description panel panel-default"]/div[@class="panel-body"]')
        description_texts = description_div.xpath('.//text()').getall()
        item['description'] = ' '.join([text.strip() for text in description_texts if text.strip()])
        # Extract and clean the phone number and email address
        item['phone_number'] = response.xpath('//div[@class="row tel"]//a/@href').get()[5:]
        item['email'] = response.xpath('//div[@class="row email"]//a/@href').get()[7:]

        yield item

