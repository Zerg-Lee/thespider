import scrapy
from xker.items import XkerItem
from scrapy.http import Request

class XkerspSpider(scrapy.Spider):
    name = "xkerSp"
    allowed_domains = ["www.xker.com"]
    start_urls = ["https://www.xker.com/c/"]

    def parse(self,response):
        '''
        url_all = ["https://www.xker.com/a/{}.html".format(i) for i in range(1,54570)]
        '''
        url_page = ["https://www.xker.com/c/{}".format(b)  + "/page/{}".format(a) for b in ['news','keji','blockchain','edu','tutorials','zhishi'] for a in range(1,6)  ]
        print(url_page)
        for i in url_page :
            yield Request(url=i.replace("/page/1","") , callback=self.parse_page , dont_filter = True)
        

    def parse_page(self,response):
        for url_text in ["/html/body/div[1]/div/div/div/div[3]/ul[1]/li[{}]/div[last()]/h2//@href".format(c) for c in range(1,11)]:
            i = response.xpath(url_text).extract()[0]
            yield Request(url=i , callback=self.parse_text , dont_filter = True)



    def parse_text(self, response):

        item = XkerItem()

        title = response.xpath('/html/body/div[1]/div/main/article/div[1]/div[1]/h1//text()').extract()
        times = response.xpath('/html/body/div[1]/div/main/article/div[1]/div[1]/div/time//text()').extract()
        contents = response.xpath('/html/body/div[1]/div/main/article/div[1]/div[2]//text()').extract()
        if len(title) == 1 :
          item['title'] = title[0]
          item['time'] = times[0].replace(" ","").replace("\n","").replace("\r","")
          item['contents'] = ''
          for each in contents:
            item['contents'] += each.replace(" ","").replace("\n","").replace("\r","")
          return item