import scrapy
from bs4 import BeautifulSoup

from .. import utils


class GoogleResearchSpider(scrapy.Spider):
    """Spider which collects items about Google research papers, authors, downloads document files and image files"""

    name = 'google-research-spider'
    start_urls = ['https://research.google.com/pubs/papers.html']

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

        soup = BeautifulSoup(response.body, "lxml")
        for row in soup.find_all(class_='pub-title'):
            if row.a:
                research_paper_url = utils.get_domain(response) + row.a.get('href')
                yield scrapy.Request(url=research_paper_url, callback=GoogleResearchPaperParser().parse)
                authors_urls = [utils.get_domain(response) + a['href'] for a in row.findNext('p').find_all('a')]
                for url in authors_urls:
                    yield scrapy.Request(url=url, callback=GoogleResearchAuthorParser().parse)
                break  # break after first yield, use in dev to scrape just 1 item


class GoogleResearchAuthorItem(scrapy.Item):
    """Item that defines a Google Research Author"""

    name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class GoogleResearchPaperItem(scrapy.Item):
    """Item that defines a Google Research Paper"""

    title = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class GoogleResearchAuthorParser(object):
    """Parser class that parsers information about an google research author, to be used by spiders"""

    item_class = GoogleResearchAuthorItem

    def parse(self, response):
        """Default method used by parser class to parse page"""

        item = self.item_class()

        name = scrapy.Selector(text=response.body).xpath("//*[@id='maia-main']/h1/text()").extract()[0]
        item['name'] = name.strip()
        image_urls = scrapy.Selector(text=response.body).xpath("//*[@id='maia-main']/div[3]/div["
                                                               "1]/div/div/div/img/@src").extract()
        image_urls = [utils.get_domain(response) + url for url in image_urls]
        item['image_urls'] = image_urls
        yield item


class GoogleResearchPaperParser(object):
    """Parser class that parsers information about an google research paper, to be used by spiders"""

    item_class = GoogleResearchPaperItem

    def parse(self, response):
        """Default method used by parser class to parse page"""

        title = scrapy.Selector(text=response.body).xpath('//*[@id="maia-main"]/h1/text()').extract()[0]
        item = self.item_class()
        item['title'] = title.strip()
        file_urls = scrapy.Selector(text=response.body).xpath('//*[@id="maia-main"]/div[3]/div[2]/div/h2/a['
                                                              '2]/@href').extract()
        file_urls = [utils.get_domain(response) + url for url in file_urls]
        item['file_urls'] = file_urls
        return item
