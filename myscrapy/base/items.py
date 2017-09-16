import scrapy
import uuid as uuid


class BaseItem(scrapy.Item):
    """
    Base Item class for this project, includes fields that all Items should have, defined by the project goal.
    """

    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)

        # set default value of a field
        for field in self.fields:
            if 'default' in self.fields[field]:
                self[field] = self.fields[field]['default']

    uuid = scrapy.Field()
    source_url = scrapy.Field()
