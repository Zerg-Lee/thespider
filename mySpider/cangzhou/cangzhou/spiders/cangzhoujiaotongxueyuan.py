import scrapy
import re
import time
from scrapy.http import Request
from cangzhou.items import CangzhouItem

class CangzhoujiaotongxueyuanSpider(scrapy.Spider):
    name = 'cangzhoujiaotongxueyuan'
    allowed_domains = ["www.bjtuhbxy.edu"]
    start_urls = ["http://www.bjtuhbxy.edu.cn/xwzx/xxtt.htm"]
    def parse(self, response):
        for url_beg in ["/html/body/div/div/div[4]/div[1]/div/ul/li[{}]/a//@href".format(i) for i in range(1, 7)]:
            url_front = ["http://www.bjtuhbxy.edu.cn/xwzx/" + response.xpath(url_beg).extract()[0].replace(".htm","")+ "/{}.htm".format(i) for i in range(1,136+1)]
            for i in url_front:
                yield scrapy.Request(url=i, callback=self.get_the_article_list, dont_filter = True)

    def get_the_article_list(self,response):
        url_article_lists = ['//*[@id="wrapper"]/div/div[4]/div[2]/div[2]/ul//li[@style != "display: none;"]/a/@href']
        for article_list in url_article_lists:
            if response.xpath(article_list).extract() != []:
              i = "http://www.bjtuhbxy.edu.cn"+response.xpath(article_list).extract()[0].replace("../..","")
              yield scrapy.Request(i, callback=self.parse_text, dont_filter = True)

    def parse_text(self, response):
        item = CangzhouItem()
        title = response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[1]//text()').extract()
        if len(title):
           

         raw_time_data = response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[2]/text()[1]').extract_first()
         unchinese_raw_time_data = re.sub('[\u4e00-\u9fa5]','',raw_time_data)
         time_raw = unchinese_raw_time_data.split( )[1] +" "+ unchinese_raw_time_data.split( )[2]
         time_array = time.strptime(time_raw, "%Y%m%d %H:%M")
         time_data = time.strftime("%Y/%m/%d %H:%M", time_array)
         #print(time_data)
        
         raw_account = response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[2]/text()[1]').extract_first()
         chinese_raw_data = re.sub('[^\u4e00-\u9fa5]','',raw_account)
         chinese_clean_1_data = re.sub('\u6587\u7ae0\u6765\u6e90','',chinese_raw_data)
         chinese_clean_2_data = re.sub('\u5e74\u6708\u65e5\u70b9\u51fb','',chinese_clean_1_data)
         #print(chinese_clean_2_data)

         contents= response.xpath('//*[@id="vsb_content_2"]/div//text()').extract()
         content = ''
         for each in contents:
             content += each.replace("\n","").replace("\r","")
         #print(content)

         item['title'] = response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[1]//text()').extract()[0]
         item['pubdate'] = time_data
         item['account'] = chinese_clean_2_data
         item['content'] = content
         item['url'] = response.url
         return item
