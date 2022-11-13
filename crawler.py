import requests
from lxml import etree
from datetime import datetime
from time import sleep

class Crawler(object):
    def __init__(
        self,
        base_url='https://www.csie.ntu.edu.tw/news/',
        rel_url='news.php?class=101',
    ):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(
        self, 
        start_date, 
        end_date,
    ):
        contents = []
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, 
                end_date, 
                page=f'&no={page_num}',
            )
            page_num += 10
            if rets:
                contents += rets
            if last_date < start_date:
                break
        contents = sorted(contents)[::-1]
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page

        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num

        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """
        res = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'},
        ).content.decode()
        sleep(0.1)

        root = etree.HTML(res)
        
        dates = root.xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]/text()")
        titles = root.xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/text()")
        rel_urls = root.xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/@href")
        
        contents = []
        last_date = datetime(1900, 1, 1)
        for date, title, rel_url in zip(dates, titles, rel_urls):
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            if (date_obj > last_date):
                last_date = date_obj
            if (date_obj < start_date or date_obj > end_date):
                continue
            date = datetime.strftime(date_obj, "%Y-%m-%d")
                
            url = self.base_url + rel_url
            content = self.crawl_content(url)
            contents.append([date, title, content])
        return contents, last_date

    def crawl_content(self, url):
        res = requests.get(url).content.decode()
        sleep(0.1)
        root = etree.HTML(res)
        content_obj = root.xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[@class=\"editor content\"]")
        content = "".join(content_obj[0].itertext())
        return content
