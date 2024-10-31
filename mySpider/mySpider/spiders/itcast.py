import scrapy


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["www.itcast.cn"]
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml"]

    def parse(self, response):
        print(response.text)
'''
class Opp2Spider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.com']
    start_urls = ['http://www.itcast.cn/']

    def parse(self, response):
        context = response.xpath('/html/head/title/text()')   
        title = context.extract_first()  
        print(title) 
        pass
    '''
