import scrapy


class xkerItem(scrapy.Item):
   title = scrapy.Field()
   author = scrapy.Field()
   content = scrapy.Field()
   pass
