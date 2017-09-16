import scrapy


class BaseItem(scrapy.Item):
    """
    Base Item class for this project, includes fields that all Items should have, defined by the project goal.
    """

    uuid = scrapy.Field()
    source_url = scrapy.Field()
