import json
import re
import scrapy
from abc import ABC

from Test.utils.process_item import clean_item


class TestSpider(scrapy.Spider, ABC):
    name = 'spider_md5'
    web_name = 'spider_name'
    custom_settings = {'LOG_FILE': './spiders/logs/spider_md5.txt'}
    url = 'https://www.zuzhirenshi.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.576',
    }
    web_data = {'web_id': 'spider_md5', 'web_name': 'spider_name'}
    count = 0
    data_lis = []

    def start_requests(self):
        yield scrapy.Request(self.url, headers=self.headers, callback=self.get_category_lists)

    def get_category_lists(self, response):
        the_category_url_lists = response.xpath('/html/body/div[4]/div/ul/li/a/@href').extract()
        for category_url_list in the_category_url_lists:
            url = "https://www.zuzhirenshi.com" + category_url_list
            yield scrapy.Request(url, callback=self.get_the_article_lists, dont_filter=True)

    def get_the_article_lists(self, response):
        header = {'Content-Type': 'application/json'}
        num_of_category = re.sub('[a-zA-Z]', '', str(response.url)[-5:])
        url = "https://www.zuzhirenshi.com/api/welcome/selectColumn"
        if num_of_category != '':
            post_data = {"id": num_of_category}
            yield scrapy.Request(url, method="post", headers=header, body=json.dumps(post_data),
                                 callback=self.get_the_article_urls,
                                 dont_filter=True)

    def get_the_article_urls(self, response):
        data_lists = json.loads(response.text)
        for one_data in data_lists['data']['listMap']:
            url = "https://www.zuzhirenshi.com/api/welcome/selectNews?id=" +one_data['columnId']
            yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)


    def parse_detail(self, response):
        title = ''.join([i for i in re.findall('showTitle":(.*?),"newName', response.text)])
        pubdate = ''.join([i for i in re.findall('"createTime":(.*?),"updateBy"', response.text)])
        content = ''.join([i for i in re.findall('newContent":(.*?),"checkPass"', response.text)])
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
                yield data
