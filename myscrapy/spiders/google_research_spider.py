import scrapy


class GoogleResearchSpider(scrapy.Spider):
    name = 'google-research-spider'
    start_urls = []

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        pass
