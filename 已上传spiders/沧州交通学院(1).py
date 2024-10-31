import scrapy, json, re, requests
from Test.utils.process_date import ParseDate
from pykafka import KafkaClient
import time
from Test.utils.process_url import check_url, parse_url, create_next_url, check_file_url
import requests, scrapy, json, datetime, os, logging, random
from Test.utils.process_item import clean_item, ProcessJson
from Test.utils.tools import filter_duplication


# noinspection PyAbstractClass


# 沧州交通学院
class TestSpider(scrapy.Spider):
    name = 'a508697bce3d0e72dfb9dbc33576abaf'
    web_name = '沧州交通学院'
    custom_settings = {'LOG_FILE': './spiders/logs/cangzhouSplog.txt'}
    url = 'http://www.bjtuhbxy.edu.cn/xwzx/xxtt.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.576',
    }
    web_data = {'web_id': 'a508697bce3d0e72dfb9dbc33576abaf', 'web_name': '沧州交通学院'}
    count = 0
    data_lis = []

    def start_requests(self):
        yield scrapy.Request(self.url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        data_list = response.xpath('//div[@class="contents-table"]/ul/li/a/@href').extract()
        for data in data_list:
            url = 'http://www.bjtuhbxy.edu.cn/xwzx/' + data
            yield scrapy.Request(url, callback=self.get_the_article_list, dont_filter=True)

        # for url_beg in ["/html/body/div/div/div[4]/div[1]/div/ul/li[{}]/a//@href".format(i) for i in range(1, 7)]:
        #     url_front = ["http://www.bjtuhbxy.edu.cn/xwzx/" + response.xpath(url_beg).extract()[0].replace(".htm",
        #                                                                                                    "") + "/{}.htm".format(
        #         i) for i in range(1, 134 + 1)]
        #     for i in url_front:
        #         yield scrapy.Request(url=i, callback=self.get_the_article_list, dont_filter=True)

    def get_the_article_list(self, response):
        article_lists = response.xpath('//li[contains(@id,"line_")]/a/@href').extract()
        for article in article_lists:
            url = check_file_url('http://www.bjtuhbxy.edu.cn/', article)
            yield scrapy.Request(url['new_url'], callback=self.parse_detail, dont_filter=True)

        # url_article_lists = ['//*[@id="wrapper"]/div/div[4]/div[2]/div[2]/ul//li[@style != "display: none;"]/a/@href']
        # for article_list in url_article_lists:
        #     if response.xpath(article_list).extract():
        #         i = "http://www.bjtuhbxy.edu.cn" + response.xpath(article_list).extract()[0].replace("../..", "")
        #         yield scrapy.Request(i, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):

        title = ''.join(response.xpath('//form[@name="_newscontent_fromname"]/div[1]/div[1]/text()').extract())
        rule_content = '文章来源：[\s\S]*?&nbsp;(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2})'
        pubdate = ''.join([i for i in re.findall(r'''%s''' % rule_content, response.text)]).strip()
        content = ''.join(response.xpath('//div[@id="vsb_content"]//p//text()').extract())
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

        # title = response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[1]//text()').extract()
        # if len(title):
        #
        #     raw_time_data = response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[2]/text()[1]').extract_first()
        #     unchinese_raw_time_data = re.sub('[\u4e00-\u9fa5]', '', raw_time_data)
        #     time_raw = unchinese_raw_time_data.split()[1] + " " + unchinese_raw_time_data.split()[2]
        #     time_array = time.strptime(time_raw, "%Y%m%d %H:%M")
        #     time_data = time.strftime("%Y/%m/%d %H:%M", time_array)
        #     # print(time_data)
        #
        #     raw_account = response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[2]/text()[1]').extract_first()
        #     chinese_raw_data = re.sub('[^\u4e00-\u9fa5]', '', raw_account)
        #     chinese_clean_1_data = re.sub('\u6587\u7ae0\u6765\u6e90', '', chinese_raw_data)
        #     chinese_clean_2_data = re.sub('\u5e74\u6708\u65e5\u70b9\u51fb', '', chinese_clean_1_data)
        #     # print(chinese_clean_2_data)
        #
        #     contents = response.xpath('//*[@id="vsb_content_2"]/div//text()').extract()
        #     content = ''
        #     for each in contents:
        #         content += each.replace("\n", "").replace("\r", "")
        #     # print(content)
        #
        # item['title'] = "".join(response.xpath('//*[@id="wrapper"]/div[4]/div[2]/form/div/div[1]//text()').extract()[0])
        # item['pubdate'] = "".join(time_data)
        # item['account'] = "".join(chinese_clean_2_data)
        # item['content'] = "".join(content)
        # item['url'] = response.url
        if item['title'] and item['content']:
            data_lis = clean_item([item])
            for data in data_lis:
                # yield data
                print(data)
