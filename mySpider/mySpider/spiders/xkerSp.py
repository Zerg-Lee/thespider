import scrapy

class XkerspSpider(scrapy.Spider):
    name = "xker"
    allowed_domains = ["www.xker.com"]
    start_urls = ["https://www.xker.com"]
    
    custom_settings = {
    'LOG_LEVEL': 'DEBUG',
    "DEFAULT_REQUEST_HEADERS": {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    }
    def parse(self, response):
        print(response.text)
'''
class XkerspSpider(scrapy.Spider):
    name = "xker"
    allowed_domains = ["xker.com"]
    start_urls = ["https://www.xker.com/a/1.html"]

    def parse(self, response):
        context = response.xpath('/html/head/title/text()')
        title = context.extract_first()  
        print(title)
        pass
'''