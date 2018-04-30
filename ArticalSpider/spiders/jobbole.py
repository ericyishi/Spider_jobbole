# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticalSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticalSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            # 帖子的url地址
            post_url = post_node.css("::attr(href)").extract_first("")
            # 贴子的封面图的url
            image_url = post_node.css("img::attr(src)").extract_first("")
            # 将控制权交给Scrapy的Request根据帖子的url进行下载
            # 回调函数callback后面跟的是进入页面后，进行处理的函数
            # Request中meta参数的作用是传递信息给下一个函数（这里就是回调parse_detail）
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:#如果有下一页那么就递归调用
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        # 这个页面已经进入每个帖子详情页了
        # 通过response.meta.get方式获取meta传过来的值
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
         # 通过item loader加载item
         # 实例化一个容器，接收item实例和response参数
         # 这里自己实例化了一个item叫JobBoleArticalItem（在items中定义的）
         # 也就是把值，装到JobBoleArticalItem中去
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
         # 这里是调用自定义的get_md5方法,将此作为id，方便以后查找
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        # 加载load_item()
        article_item = item_loader.load_item()
        # yield将这个item返给scrapy,传给pipelines，但是需要在setting中开启
        yield article_item

