import scrapy

from .. import utils


class GoogleResearchSpider(scrapy.Spider):
    """Spider which collects items about Google research papers, authors, downloads document files and image files"""

    name = 'google-research-spider'
    start_urls = []

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        return self.parse_publications_research_areas(response)

    def parse_publications_research_areas(self, response):
        """Parse publications page to extract research area URLs and make requests to those pages"""

        research_area_urls = scrapy.Selector(text=response.body).xpath('//*[@id="maia-main"]/div[3]/div[2]/div['
                                                                       '1]/div/ul//li/a/@href').extract()
        # Correct URLs, add domain
        domain = utils.get_domain(response)
        research_area_urls = [domain + url for url in research_area_urls]

        # Yield requests with parsed research area URLs
        for research_area_url in research_area_urls:
            yield scrapy.Request(url=research_area_url, callback=self.parse_research_area)
            break  # break after first yield, use in dev to scrape just 1 item

    def parse_research_area(self, response):
        """Parse research area page to extract paper items (incomplete paper item) + their PDFs  and/or paper URLs and
        author items"""


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
