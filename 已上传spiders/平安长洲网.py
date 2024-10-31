import scrapy
from abc import ABC
from Test.utils.process_item import clean_item


class TestSpider(scrapy.Spider, ABC):
    name = 'b20a52f4e96deda55c85c99c3491946a'
    web_name = '平安长洲网'
    custom_settings = {'LOG_FILE': './spiders/logs/平安长州网log.txt',
                       'CONCURRENT_REQUESTS': 1,
                       'DOWNLOAD_DELAY': 0.3,
                       'RANDOMIZE_DOWNLOAD_DELAY': True,
                       }
    url = 'http://changzhou.pawz.gov.cn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.576',
    }
    web_data = {'web_id': 'b20a52f4e96deda55c85c99c3491946a', 'web_name': '平安长洲网'}
    count = 0
    data_lis = []

    def start_requests(self):
        yield scrapy.Request(self.url, headers=self.headers, callback=self.get_category_lists)

    def get_category_lists(self, response):
        the_category_url_lists = response.xpath('/html/body/div[2]/div/ul/li/a/@href').extract()
        for category_url_list in the_category_url_lists:
            category_url = 'http://changzhou.pawz.gov.cn/' + category_url_list.replace("./", "")
            yield scrapy.Request(category_url, callback=self.get_the_article_lists, dont_filter=True)

    def get_the_article_lists(self, response):
        the_article_url_lists = response.xpath("/html/body/div[3]/div/div[2]//@href").extract()
        for the_article_url_list in the_article_url_lists:
            article_url = 'http://changzhou.pawz.gov.cn/' + the_article_url_list.replace("./", "")
            yield scrapy.Request(article_url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        title = ''.join(response.xpath('//*[@id="activity-name"]/text()').extract())
        pubdate = ''.join(response.xpath('//*[@id="meta_content"]//text()').extract())
        content = ''.join(response.xpath('//*[@id="js_content"]//text()').extract())
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
