import scrapy


class WebdealSpider(scrapy.Spider):
    name = 'webdeal'
    allowed_domains = ['webdeal.cz']
    start_index = 0
    search_url = 'https://www.webdeal.cz/poptavky?sort=&start={}'
    start_urls = [search_url.format(start_index)]

    def parse(self, response):
        records = response.xpath('//table/tr')
        # End in case of no more results
        if len(records) == 1 and not records.xpath('td[1]/a'):
            # table contains only simple text of "no more results" message
            return

        for record in records:
            url = record.xpath('td[1]/a').attrib["href"]
            title = record.xpath('td[1]/a/text()').get()
            price = record.xpath('td[3]/text()').get()
            yield {
                'title': title,
                'price': price,
                'url': url
            }

        self.start_index += 25
        next_page_link = self.search_url.format(self.start_index)
        yield scrapy.Request(next_page_link, callback=self.parse)
