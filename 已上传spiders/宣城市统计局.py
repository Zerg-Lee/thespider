import random
import scrapy
from abc import ABC
from Test.utils.process_item import clean_item


class TestSpider(scrapy.Spider, ABC):
    name = 'b8fdf95754e14fa71cedc162376738d0'
    web_name = '宣城市统计局'
    custom_settings = {'LOG_FILE': './spiders/logs/宣城市统计局log.txt',
                       'CONCURRENT_REQUESTS': 1,
                       'DOWNLOAD_DELAY': 1,
                       }
    url = 'https://tjj.xuancheng.gov.cn'
    headers = {"User-Agent": random.choice(
        ['Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
         'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 '
         'LBBROWSER',
         'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; '
         '360SE)',
         'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET '
         'CLR 3.0.04506.30)',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 '
         'Safari/535.20',
         'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
         'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 '
         'LBBROWSER',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC '
         '5.0; .NET CLR 3.0.04506)',
         'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
         'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
         'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
         'Version/10.3 Mobile/14E277 Safari/603.1.30',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '
         'Safari/537.36']),
        'Cookie':'_gscu_1279657679 = 862154975y6qhb82;Hm_lvt_d582e9482896d49a93a28bcbe79fa753 = 1686215598, 1686273365;Hm_lvt_96da6bb9c6240d1fcc3e26827fb60319 = 1686215598, 1686273365;_gscbrs_1279657679 = 1;Hm_lvt_4613ff0fe2c71c8c6e7876a3c02442e4 = 1686215498, 1686269716, 1686273599;Hm_lpvt_4613ff0fe2c71c8c6e7876a3c02442e4 = 1686293042;_gscs_1279657679 = t86293041ioor1090 | pv:1'
    }
    web_data = {'web_id': 'b8fdf95754e14fa71cedc162376738d0', 'web_name': '宣城市统计局'}
    count = 0
    data_lis = []

    def start_requests(self):
        yield scrapy.Request(self.url, headers=self.headers, callback=self.get_the_category_lists)

    def get_the_category_lists(self, ):
        for one_data in [1580, 1588, 1589]:
            url = "https://tjj.xuancheng.gov.cn/News/showList/" + str(one_data) + '/page_1.html'
            yield scrapy.Request(url, headers=self.headers, callback=self.get_the_article_lists, dont_filter=True)

    def get_the_article_lists(self, response):
        the_article_url_lists = response.xpath("/html/body/div[3]/div[3]/div[1]/ul/li/a/@href").extract()
        for the_article_url_list in the_article_url_lists:
            article_url = 'https://tjj.xuancheng.gov.cn' + the_article_url_list
            yield scrapy.Request(article_url, headers=self.headers, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        title = ''.join(response.xpath('/html/body/div[3]/div[2]/h1/text()').extract())
        pubdate = ''.join(
            response.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/span[4]/text()').extract().replace('发布时间：', ''))
        content = ''.join(response.xpath('//*[@id="zoom"]//text()').extract())
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
