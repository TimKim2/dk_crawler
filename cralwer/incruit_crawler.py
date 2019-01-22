from cralwer.super_crawler import SuperCrawler
from cralwer.people import People
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pandas import DataFrame
from collections import defaultdict


class IncruitCrawler(SuperCrawler):
    def __init__(self):
        super(IncruitCrawler, self).__init__()
        self.repeat_count = 10

        self.first_business_category = ''
        self.second_business_category = ''
        self.occupational_category = ''
        self.area_category = ''
        self.detail_area_category = ''
        self.sex_category = ''
        self.read_number = 1

        self.people_list = []

        self.file_link = ''

        self.excel_list = []

    def load_page(self):
        self.url_action('http://resumedb.incruit.com/list/searchresume.asp?where=All')
        self.wait_action('//*[@id="searchForm"]/div[2]/div[2]/div[2]/div[2]/table/tbody')

    def set_condition(self):
        pass

    def crawling_resume(self):

        count = 0
        current_page = 1

        while True:
            for i in range(0, 50):
                try:
                    people_dict = defaultdict(str)
                    people_dict['URL'] = self.enter_page('//*[@id="searchForm"]/div[2]/div[2]/div[2]/div[2]/'
                                                         'table/tbody/tr[' + str((count % 50) + 1) + ']/th/div/h3/a')

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

            self.select_page(str(current_page))
            current_page += 1

    def make_csv(self):
        df = DataFrame(self.csv_data, columns=['URL', '나이', '희망업종', '희망직종', '희망연봉', '현재상태',
                                               '근무지역선택'])

        today_time = datetime.today().strftime("%Y%m%d%H%M")

        export_csv = df.to_csv('csv/' + today_time + '.csv', index=None, header=True)

        self.file_link = 'http://ec2-54-180-142-25.ap-northeast-2.compute.amazonaws.com:8888/edit/notebook/csv/' \
                         + today_time + '.csv'

        print("링크")
        print('http://ec2-54-180-142-25.ap-northeast-2.compute.amazonaws.com:8888/edit/notebook/csv/'
              + today_time + '.csv')

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
        page_list = self.find_elements('//*[@id="Table3"]/tbody/tr[2]/td/a')

        for i in page_list:
            if page_number in i.text:
                i.click()
                self.wait_action('//*[@id="Table4"]/tbody/tr[6]')
                return

    def get_age(self, xpath):
        age_element = self.find_element(xpath)

        people_info = age_element.text
        people_info = people_info.split('\n')
        people_age = people_info[1]

        people_age = people_age.replace('(', '')
        people_age = people_age.replace(')', '')

        return people_age

    def enter_page(self, xpath):
        button = self.find_element(xpath)

        link_url = button.get_property('href')
        self.url_action(link_url)

        return link_url


if __name__ == '__main__':
    crawler = TradeinCrawler()
    crawler.init_condition('무역서비스업', '판매', '오더관리', '경기', '가평군', '남', 60)
    crawler.run()
