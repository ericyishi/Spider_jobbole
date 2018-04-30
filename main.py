from scrapy.cmdline import execute
import sys
import os

# 将文件放入path路径下才能调试
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 启动爬虫，格式：scrapy crawl spider名字
execute(["scrapy", "crawl", "jobbole"])
