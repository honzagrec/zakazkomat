import re
import scrapy

from datetime import date

LIMIT_DAYS = 100    # Since ePoptavka doesn't remove old listings, parse only X days

class EpoptavkaSpider(scrapy.Spider):
    name = 'epoptavka'
    allowed_domains = ['epoptavka.cz']
    start_urls = ['https://poptavky.epoptavka.cz/pocitace-software-vyvoj-aplikaci/1']

    def parse(self, response):
        records = response.xpath('//div[contains(@class, "stripped-list")]/div')
        for record in records:
            # If record is too old - stop crawling
            if LIMIT_DAYS:
                added_str = record.xpath('*/ul/li[1]/text()').get().strip()
                day, month, year = re.findall("[0-9]+", added_str)
                added = date(int(year), int(month), int(day))
                record_age = date.today() - added
                if record_age.days > LIMIT_DAYS:
                    break


            url = record.xpath('*/a').attrib["href"]
            title = record.xpath('*//h4/span/text()').get().strip()
            yield {
                'title': title,
                'url': url
            }
        else:
            # Go to next page only when there was no record onlder than LIMIT_DAYS,
            #   otherwise just end - all following crawling would return older records
            next_page = response.xpath('//a[@rel="next"]')
            if next_page:
                next_page_link = next_page.attrib["href"]
                yield scrapy.Request(next_page_link, callback=self.parse)
