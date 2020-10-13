# -*- coding: gbk -*-
from scrapy.spiders import CrawlSpider
import scrapy
from urllib.parse import urljoin


class MovieDetailSpider(CrawlSpider):
    name = "flim"
    allowed_domains = ["endata.com.cn"]

    def start_requests(self):
        start_url = 'https://www.endata.com.cn/BoxOffice/MovieStock/movies.html'
        self.page = 1
        self.max_page = 500
        yield scrapy.Request(start_url, self.parse, dont_filter=True, meta={
            'page': self.page,
        })

    def parse(self, response):
        li_movie_list = response.css('ul.movies-list-box li')
        for li_movie_info in li_movie_list:
            relative_url = li_movie_info.css('a::attr(href)').extract_first()
            relative_url = relative_url.strip()
            movie_url = urljoin(response.url, relative_url)
            yield scrapy.Request(movie_url, callback=self.movie_detail_page,
                                 dont_filter=False)  # when you run, turn to True
        start_url = 'https://www.endata.com.cn/BoxOffice/MovieStock/movies.html'
        self.page += 1
        if self.page < self.max_page:
            yield scrapy.Request(start_url, self.parse, dont_filter=True, meta={
                'page': self.page,
            })

    def movie_detail_page(self, response):
        try:
            movie_dict = {'url': response.url}
            movie_info_div = response.css('div#Minfo')
            name_box_div = movie_info_div.css('div.rbox1')
            ch_name: str = name_box_div.css('h3::text').extract_first()
            movie_dict['ch_name'] = ch_name.strip()
            en_name: str = name_box_div.css('p.en::text').extract_first()
            movie_dict['en_name'] = en_name.strip()
            total_box_office: str = movie_info_div.css('div.boxs strong::text').extract_first()
            movie_dict['total_box_office'] = total_box_office
            other_info = movie_info_div.css('div.bt-info')
            info_list = other_info.css('p::text').extract()
            # get all info
            movie_dict['type_info'] = info_list[0].split('：')[-1]
            movie_dict['make_type'] = info_list[1].split(':')[-1]
            movie_dict['minute'] = info_list[2].split(':')[-1].strip()
            movie_dict['public_time'] = info_list[3].split('：')[-1]
            movie_dict['public_country'] = info_list[4].split('：')[-1]
            movie_dict['publisher_company'] = other_info.css('a')[-1].css('::text').extract_first()

            # data
            movie_data_dl = response.css('dl#mv-Basic')
            if movie_data_dl:
                main_actor_list = []
                company_list = []
                main_actors = movie_data_dl.css('dd a::text').extract()
                for actor in main_actors:
                    if actor.find('公司') != -1:
                        if actor not in company_list:
                            company_list.append(actor)
                    elif actor not in main_actor_list:
                        main_actor_list.append(actor)
                movie_dict['actors'] = ";".join([str(i) for i in main_actors])
                movie_dict['companies'] = ";".join([str(i) for i in company_list])

            # box office
            box_tbody = response.css('div#mv-Box tbody')
            if box_tbody:
                box_tr = box_tbody.css('tr')[1:]
                box_str = ''
                for single_box_tr in box_tr:
                    box_td = single_box_tr.css('td')
                    box_week = box_td[0].css('span::text').extract_first()
                    box_info_list = single_box_tr.css('td::text').extract()[1:]
                    box_str += box_week + "_" + "_".join(str(i).strip() for i in box_info_list) + ";"
                # [time,population per play,box office pre week, box office total,play day]
                box_str = box_str.replace(',', '，')
                box_str = box_str.replace('\n', '')
                movie_dict['box_office'] = box_str
            event_div = response.css('div#marketBox')
            if event_div:
                event_li = event_div.css('div.smarket-list ul li')
                movie_str = ''
                try:
                    for single_event in event_li:
                        time = single_event.css('::attr(datet)').extract_first()
                        relative_time = single_event.css('span.sdate::text').extract_first()
                        news_url = single_event.css('div.conbox a::attr(href)').extract_first()
                        news_title = single_event.css('div.conbox a::text').extract_first()
                        news_content = single_event.css('div.txt::text').extract_first()
                        relative_time = relative_time.strip() if relative_time else ""
                        news_url = news_url.strip() if news_url else ""
                        news_title = news_title.strip() if news_title else ""
                        news_content = news_content.strip() if news_content else ""
                        movie_str += time + "_" + relative_time + '_' + news_url + "_" + news_title + '_' + news_content + ';'
                except Exception as e:
                    print(e)
                movie_str = movie_str.replace(',', '，')
                movie_str = movie_str.replace('\n', '')
                movie_dict['event'] = movie_str
                yield movie_dict
        except Exception as e:
            print(e)
