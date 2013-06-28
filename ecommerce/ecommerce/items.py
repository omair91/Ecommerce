from scrapy.item import Item, Field

class EcommerceItem(Item):
    name = Field()
    description = Field()
    image_urls = Field()
    price = Field()
    source_url = Field()
    images = Field()