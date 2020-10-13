import sys
import os
from scrapy.cmdline import execute

# 直接运行这个python文件,即可在程序中调试
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 第三个参数是spider的name
execute(['scrapy', 'crawl', 'flim'])