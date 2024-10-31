import json
import scrapy
from abc import ABC
from Test.utils.process_item import clean_item


class TestSpider(scrapy.Spider, ABC):
    name = 'af08c97eafcde8e4efda02c9d1a94c49'
    web_name = '菏泽市文化和旅游局'
    custom_settings = {'LOG_FILE': './spiders/logs/菏泽市文化和旅游局log.txt'}
    url = 'http://whly.heze.gov.cn/wlxwdt/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.576',
    }
    web_data = {'web_id': 'af08c97eafcde8e4efda02c9d1a94c49', 'web_name': '菏泽市文化和旅游局'}
    count = 0
    data_lis = []

    def start_requests(self):
        yield scrapy.Request(self.url, headers=self.headers, callback=self.get_the_article_lists)

    def get_the_article_lists(self, response):
        header = {'Content-Type': 'application/json',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.576', }
        url = "http://whly.heze.gov.cn/els-service/article/1/15"
        for catas in ['1585095198864707584', '1585095253789118464', '1585095322663784448', '1585106982950539264']:
            post_data = {"dw": ["2c908088819842f701819a25e5c4001d"], "type": [1], "fwzt": "3", "order": "fwdate",
                         "catas": [catas]}
            yield scrapy.Request(url, method="post", headers=header, body=json.dumps(post_data),
                                 callback=self.get_the_article_urls, dont_filter=True)

    def get_the_article_urls(self, response):
        data_lists = json.loads(response.text)
        for one_data in data_lists['data']['contents']:
            url ='http://whly.heze.gov.cn/'+str(one_data['dwid'])+'/'+str(one_data['xxid']+'.html')
            yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        title = ''.join(response.xpath('//*[@id="wrapper"]/div[4]/div/div[2]/table/tbody/tr[3]/td[2]//text()').extract())
        pubdate = ''.join(response.xpath('//*[@id="wrapper"]/div[4]/div/div[2]/table/tbody/tr[3]/td[4]//text()').extract()).replace(' ', '')
        content = ''.join(response.xpath('//*[@id="ozoom"]/p//text()').extract())
        item = {
            'title': title,  # 标题
            'pubdate': pubdate,  # 发布时间
            'content': content,  # 内容
            'account': '',  # 作者
            'original_url': '',  # 原文链接
            'head_url': '',  # 头像图片
            'summary': '',  # 摘要
            'transmit_count': '',  # 转发量
            'comment_count': '',  # 评论量
            'like_count': '',  # 点赞量
            'web_id': self.web_data['web_id'],  # 网站id
            'web_name': self.web_data['web_name'],  # 网站名
            'url': response.url,  # 文章链接
            'media_type': 0,  # 媒体分类（0:国内新闻网站,1:论坛,2:博客,3:网站,4:视频,5:境外网站,9:问答,10:报刊,12:贴吧,13:微博,14:微信,16:境外微博,）
            'is_foreign': 0,  # 是否为境外（1是 0否）
            'data_source': 1,  # 数据分类1.网站 2.app
            "html": response,
        }
        if item['title'] and item['content']:
            data_lis = clean_item([item])
            for data in data_lis:
                # yield data
                print(data)
