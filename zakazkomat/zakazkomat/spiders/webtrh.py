import scrapy


class WebtrhSpider(scrapy.Spider):
    name = 'webtrh'
    allowed_domains = ['webtrh.cz']
    start_urls = ['https://webtrh.cz/f101/page1?sort=creationdate&order=desc']

    def parse(self, response):
        records = response.xpath('//div[contains(@class, "deal-row item")]')
        for record in records:
            link_elem = record.xpath('*/a')[0]
            url = link_elem.attrib["href"]
            title = link_elem.get().split('\n')[-2].strip()
            price = record.xpath('*/span[@class="value"]/text()').get().strip()
            yield {
                'title': title,
                'price': price,
                'url': url
            }

        next_page = response.xpath('//span[@class="last"]/a')
        if next_page:
            next_page_link = 'https://webtrh.cz' + next_page.attrib["href"]
            yield scrapy.Request(next_page_link, callback=self.parse)
