# 艺恩网爬虫使用说明

This is a endata (https://www.endata.com.cn/BoxOffice/MovieStock/movies.html) spider built by scrapy

endata.com.cn have a movie database, which contains video data, box office, news and other information.

这是一个由 scrapy+selenium 构建的艺恩网爬虫，爬取内容如下：https://www.endata.com.cn/BoxOffice/MovieStock/movies.html ，页面进入后展示出的全部电影与点进电影后的全部内容。


# 使用方法

- pip install scrapy pandas
- 配置 chromedriver
    
    Mac配置chromedriver：https://blog.csdn.net/weixin_35757704/article/details/108893407
    
    Linux配置chromedriver:https://blog.csdn.net/weixin_35757704/article/details/105583063
    
- 运行 ```python movie_data/main.py```，如需调试程序，也可以 debug main.py 这个文件


# 文件说明

本项目遵循scrapy架构编码，不同功能分别放在不同的文件中

- spiders文件夹下：
    - film_page_url.py 文件：核心爬虫文件

- middlewares.py 文件：爬取链接的中间件，使用selenium的chromedriver爬取
- pipelines.py 文件：保存数据，这里我使用pandas保存到movie2020_url.csv 文件中，可以自定义
