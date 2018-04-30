# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
import datetime

class ArticalspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass






def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def return_value(value):
    return value

def get_nums(value):
    # 如果没有数字，那么默认为0
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

class ArticleItemLoader(ItemLoader):
    #自定义itemloader继承于ItemLoader
    default_output_processor = TakeFirst()

# 自定义了一个item，里面定义的就是需要的字段
class JobBoleArticleItem(scrapy.Item):
  title=scrapy.Field()
  create_date=scrapy.Field(
      input_processor=MapCompose(date_convert)
  )
  url=scrapy.Field()
  url_object_id=scrapy.Field()
  front_image_url=scrapy.Field(
      output_processor=MapCompose(return_value)
  )
  praise_nums=scrapy.Field(
      input_processor=MapCompose(get_nums)
  )
  comment_nums=scrapy.Field(
      input_processor=MapCompose(get_nums)
  )
  fav_nums=scrapy.Field(
      input_processor=MapCompose(get_nums)
  )
  tags=scrapy.Field()
  content=scrapy.Field()

