import scrapy


class GoogleResearchSpider(scrapy.Spider):
    """Spider which collects items about Google research papers, authors, downloads document files and image files"""

    name = 'google-research-spider'
    start_urls = []

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        pass


class GoogleResearchAuthorItem(scrapy.Item):
    """Item that defines a Google Research Author"""


class GoogleResearchPaperItem(scrapy.Item):
    """Item that defines a Google Research Paper"""


class GoogleResearchAuthorParser(object):
    """Parser class that parsers information about an google research author, to be used by spiders"""

    def parse(self, response):
        """Default method used by parser class to parse page"""


class GoogleResearchPaperParser(object):
    """Parser class that parsers information about an google research paper, to be used by spiders"""

    def parse(self, response):
        """Default method used by parser class to parse page"""
