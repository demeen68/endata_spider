# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from scrapy.http import HtmlResponse
import time


class HandlessMiddleware(object):

    def __init__(self):
        super(HandlessMiddleware, self).__init__()
        option = webdriver.ChromeOptions()

        option.add_argument('--disable-gpu')
        option.add_argument('lang=zh_CN.UTF-8')
        # option.add_argument(
        #     'user-agent=' + self.ua.random)
        option.add_argument('headless')
        prefs = {
            "profile.managed_default_content_settings.images": 2,  # 禁止加载图片
            # 'permissions.default.stylesheet': 2,  # 禁止加载css
        }
        option.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(chrome_options=option)
        self.browser.implicitly_wait(10)
        self.browser.execute_script('window.open("","_blank");')

    def process_request(self, request, spider):
        time.sleep(8)
        if request.url == 'https://www.endata.com.cn/BoxOffice/MovieStock/movies.html':
            if request.meta['page'] == 1:
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.browser.get(request.url)
                self.browser.find_element_by_id('TableList_Paging')
                self.max_page = int(self.browser.find_element_by_id('TableList_Paging').find_element_by_css_selector(
                    'a.layui-laypage-last').text)
                time.sleep(5)
            else:
                self.browser.switch_to.window(self.browser.window_handles[0])
                if request.meta['page'] <= self.max_page:
                    print("MAIN PAGE CHANGE : " + str(request.meta['page']) + " / " + str(self.max_page))
                    self.browser.find_element_by_id('TableList_Paging').find_element_by_class_name(
                        'layui-laypage-next').click()  # get next page
                else:
                    return None
        else:
            print("NEW PAGE GET : " + request.url)
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.get(request.url)
            time.sleep(5)
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8",
                            request=request)
