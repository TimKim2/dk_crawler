from cralwer.super_crawler import SuperCrawler
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pandas import DataFrame
from collections import defaultdict


class IncruitCrawler(SuperCrawler):
    def __init__(self):
        super(IncruitCrawler, self).__init__()
        self.read_number = 10
        self.people_list = []

        self.file_link = ''

        self.crawl_url = ''

        self.id = 'dnd8149'
        self.pw = 'dnd6243*'
        self.excel_list = ['URL', '최종학력', '총학력', '희망연봉', '프로필']

    def init_condition(self, crawl_url, repeat_count):
        self.crawl_url = crawl_url
        self.read_number = repeat_count

    def login_page(self):
        self.url_action('https://edit.incruit.com/login/login.asp?gotoURL=http%3A%2F%2'
                        'Frecruiter%2Eincruit%2Ecom%2Fmain%2Frecruiter%2Easp&Site=recruiter&Partner=0')

        self.wait_action('//*[@id="g_form_login_box"]/fieldset/div/ul')

        self.input_action('//*[@id="txtUserID"]', self.id)
        self.input_action('//*[@id="txtPassword"]', self.pw)

        self.click_action('//*[@id="g_form_login_box"]/fieldset/div/button')

    def set_condition(self):
        self.click_action('//*[@id="CompanyLayer"]/div/div[1]/button')
        self.url_action(self.crawl_url)
        self.wait_action('//*[@id="searchForm"]/div[2]/div[2]/div/div[2]/table/tbody')

    def crawling_resume(self):

        count = 0
        current_page = 1

        while True:
            for i in range(0, 60):
                try:
                    people_dict = defaultdict(str)
                    people_dict['URL'] = self.enter_page('//*[@id="searchForm"]/div[2]/div[2]/div/div[2]/'
                                                         'table/tbody/tr[' + str((count % 50) + 1) + ']/th/div/h3/a')

                    # self.enter_page('//*[@id="searchForm"]/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/th/div/h3/a')

                    # '//*[@id="searchForm"]/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/th/div/h3/a'

                    if self.check_alert():
                        count += 1
                        self.read_number += 1
                        continue

                    self.wait_action('//*[@id="Table8"]/tbody/tr[5]/td/table/tbody/tr/td[4]/table/'
                                     'tbody/tr/td/table/tbody/tr[4]/td/table')

                    people_dict['최종학력'] = self.get_text('//*[@id="resumeViewWrap"]/'
                                                        'div[2]/div[1]/div/div[1]/table/tbody/tr/td[1]/div/p')

                    people_dict['총학력'] = self.get_text('//*[@id="resumeViewWrap"]'
                                                       '/div[2]/div[1]/div/div[1]/table/tbody/tr/td[2]/div/p/em')

                    people_dict['희망연봉'] = self.get_text('//*[@id="resumeViewWrap"]/div[2]/div[1]/div/div[1]/'
                                                        'table/tbody/tr/td[3]/div/p/span')

                    people_dict['학력사항'] = self.get_text('//*[@id="resumeViewWrap"]/div[2]/div[2]/div/div[3]/div/h2/span')

                    people_dict['자격증'] = self.get_text('//*[@id="resumeViewWrap"]/div[2]/div[2]/div/div[8]/div[2]/table')

                    people_dict['프로필'] = self.get_text('//*[@id="resumeViewWrap"]/div[2]/div[2]/div')

                    self.go_back_page()

                    self.wait_action('//*[@id="searchForm"]/div[2]/div[2]/div[2]/div[2]/table/tbody')

                    for j in people_dict:
                        self.csv_data[j].append(people_dict[j])

                except Exception as e:
                    print(e)

                count += 1
                self.printProgress(count, self.read_number, 'Progress:', 'Complete', 1, 100)

                if count >= self.read_number:
                    break

            if count >= self.read_number:
                break

            current_page += 1
            self.select_page(current_page)

    def make_csv(self):
        df = DataFrame(self.csv_data, columns=self.excel_list)

        file_name = 'csv/incruit' + datetime.today().strftime("%Y%m%d%H%M") + '.csv'

        export_csv = df.to_csv(file_name, index=None, header=True)

        print("링크")
        print('http://ec2-54-180-142-25.ap-northeast-2.compute.amazonaws.com:8888/edit/notebook/' + file_name)

    def click_condition(self, category, xpath):
        if category == '':
            return
        self.click_action(xpath)
        option_path = xpath + '/option'
        self.wait_action(option_path)

        select_list = self.find_elements(option_path)

        for i in select_list:
            if category in i.text:
                i.click()
                break

    def select_page(self, page_number):
        self.click_action('//*[@id="searchForm"]/div[2]/div[2]/div/p/a[' + str(page_number - 1) + ']')
        self.wait_action('//*[@id="searchForm"]/div[2]/div[2]/div/div[2]/table/tbody')

    def enter_page(self, xpath):
        button = self.find_element(xpath)

        link_url = button.get_property('href')
        self.url_action(link_url)

        return link_url


if __name__ == '__main__':
    crawler = IncruitCrawler()
    crawler.init_condition('http://resumedb.incruit.com/list/searchresume.asp?where=All&SearchType=DETAIL&crr1=0&crr2=0', 2)
    crawler.run()
