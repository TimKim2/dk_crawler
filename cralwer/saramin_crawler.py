from cralwer.super_crawler import SuperCrawler
from cralwer.people import People
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pandas import DataFrame
from collections import defaultdict


class SaramInCrawler(SuperCrawler):
    def __init__(self):
        super(SaramInCrawler, self).__init__()
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

        self.excel_list = ['URL', '나이', '희망업종', '희망직종', '희망연봉', '현재상태', '근무지역선택']

    def init_condition(self, first_business_category='', second_business_category='', occupational_category='',
                       area_category='', detail_area_category='', sex_category='', read_number=50):
        self.first_business_category = first_business_category
        self.second_business_category = second_business_category
        self.occupational_category = occupational_category
        self.area_category = area_category
        self.detail_area_category = detail_area_category
        self.sex_category = sex_category
        self.read_number = read_number

    def load_page(self):
        self.url_action('http://www.tradein.co.kr/apply/apply_all.asp')
        self.wait_action('//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/'
                         'tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr[1]/td/'
                         'table/tbody/tr/td[2]/select')

    def set_condition(self):
        self.click_condition(self.first_business_category,
                             '//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/'
                             'tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr[1]/td/'
                             'table/tbody/tr/td[2]/select')

        self.click_condition(self.second_business_category,
                             '//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/'
                             'tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr[1]/td/'
                             'table/tbody/tr/td[3]/select')

        self.click_condition(self.occupational_category,
                             '//*[@id="Select3"]')

        self.click_condition(self.area_category,
                             '//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/'
                             'td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/'
                             'td[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/select[1]')

        self.click_condition(self.detail_area_category,
                             '//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[3]/td/table/'
                             'tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/select[2]')

        self.click_condition(self.sex_category,
                             '//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[3]/td/table/'
                             'tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/select')

        self.click_condition('50',
                             '//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/tbody/tr[3]/td/table/'
                             'tbody/tr/td/table/tbody/tr/td[3]/table/tbody/tr[4]/td/table/tbody/tr/td[4]/select')

        self.click_action('//*[@id="Table2"]/tbody/tr/td[2]/table[1]/tbody/tr[3]/td/table/'
                          'tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[4]/a')

        self.wait_action('//*[@id="Table4"]/tbody/tr[6]')

    def crawling_resume(self):

        count = 0
        current_page = 1

        while True:
            for i in range(0, 50):
                try:

                    people_dict = defaultdict(str)
                    people = People()

                    people_dict['나이'] = self.get_age('//*[@id="Table4"]/tbody/tr[6]/td/'
                                                     'table/tbody/tr[' + str((count % 50) * 3 + 1) + ']/td[1]')

                    people_dict['URL'] = self.enter_page('//*[@id="Table4"]/tbody/tr[6]/td/'
                                                         'table/tbody/tr[' + str((count % 50) * 3 + 1) + ']/td[4]/a')

                    if self.check_alert():
                        count += 1
                        self.read_number += 1
                        continue

                    self.wait_action('//*[@id="Table8"]/tbody/tr[5]/td/table/tbody/tr/td[4]/table/'
                                     'tbody/tr/td/table/tbody/tr[4]/td/table')

                    people_dict['희망업종'] = self.find_element('//*[@id="Table8"]/tbody/tr[5]/td/table/'
                                                            'tbody/tr/td[4]/table/tbody/'
                                                             'tr/td/table/tbody/tr[4]/td/table/'
                                                             'tbody/tr[3]/td[2]/table/tbody/'
                                                             'tr[1]/td[5]').text

                    people_dict['희망직종'] = self.find_element('//*[@id="Table8"]/tbody/tr[5]/td/table/tbody'
                                                                 '/tr/td[4]/table/tbody/tr/td/table/tbody/tr[4]/'
                                                                 'td/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td[4]').text

                    people_dict['희망연봉'] = self.find_element('//*[@id="Table8"]/tbody/tr[5]/td/table/tbody/'
                                                            'tr/td[4]/table/tbody/tr/td/table/tbody/tr[4]/'
                                                              'td/table/tbody/tr[3]/td[2]/table/tbody/tr[7]/td[4]').text

                    people_dict['현재상태'] = self.find_element('//*[@id="Table8"]/tbody/tr[5]/td/table/tbody/tr/td[4]'
                                                                 '/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/'
                                                                 'tr[3]/td[2]/table/tbody/tr[11]/td[4]').text

                    people_dict['근무지역선택'] = self.find_element('//*[@id="Table8"]/tbody/tr[5]/td/table/tbody/tr/td[4]/'
                                                             'table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[3]'
                                                             '/td[2]/table/tbody/tr[13]/td[4]').text

                    for j in self.excel_list:
                        self.csv_data[j].append(people_dict[j])

                    self.go_back_page()

                    self.wait_action('//*[@id="Table4"]/tbody/tr[6]')

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
        df = DataFrame(self.csv_data, columns=self.excel_list)

        today_time = datetime.today().strftime("%Y%m%d%H%M")

        csv_name = 'tradein_' + today_time

        export_csv = df.to_csv('csv/tradein' + today_time + '.csv', index=None, header=True)

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
    crawler.init_condition('무역서비스업', '판매', '오더관리', '경기', '가평군', '남', 2)
    crawler.run()
