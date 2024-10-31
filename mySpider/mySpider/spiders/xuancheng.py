import scrapy


class XuanchengSpider(scrapy.Spider):
    name = 'xuancheng'
    allowed_domains = ['tjj.xuancheng.gov.cn/News/showList/1580/page_1.html']
    start_urls = ['http://tjj.xuancheng.gov.cn/News/showList/1580/page_1.html']
    header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_gscu_1279657679=862154975y6qhb82; Hm_lvt_d582e9482896d49a93a28bcbe79fa753=1686215598,1686273365; Hm_lvt_96da6bb9c6240d1fcc3e26827fb60319=1686215598,1686273365; _gscbrs_1279657679=1; Hm_lvt_4613ff0fe2c71c8c6e7876a3c02442e4=1686215498,1686269716,1686273599; _gscs_1279657679=t86278458d0lsqb11|pv:7; Hm_lpvt_4613ff0fe2c71c8c6e7876a3c02442e4=1686280449',
            'Host': 'tjj.xuancheng.gov.cn',
            'If-Modified-Since': 'Thu, 08 Jun 2023 16:35:11 GMT',
            'If-None-Match': 'W/"6482033f-3c10"',
            'Referer': 'https://tjj.xuancheng.gov.cn/News/showList/1588/page_1.html',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"}

    def get_the_category_lists(self, response):
        for one_data in [1580, 1588, 1589]:
            url = "http://tjj.xuancheng.gov.cn/News/showList/" + str(one_data) + '/page_1.html'
            yield scrapy.Request(url, callback=self.get_the_article_lists, dont_filter=True)

    def get_the_article_lists(self, response):
        the_article_url_lists = response.xpath("/html/body/div[3]/div[3]/div[1]/ul/li/a/@href").extract()
        for the_article_url_list in the_article_url_lists:
            article_url = 'http://tjj.xuancheng.gov.cn' + the_article_url_list
            yield scrapy.Request(article_url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        title =response.xpath('/html/body/div[3]/div[2]/h1/text()').extract()
        pubdate = response.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/span[4]/text()').extract()
        content = response.xpath('//*[@id="zoom"]//text()').extract()
        print(title,pubdate,content)