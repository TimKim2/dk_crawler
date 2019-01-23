from cralwer.super_crawler import SuperCrawler
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pandas import DataFrame
from collections import defaultdict


class JobKoreaCrawler(SuperCrawler):
    def __init__(self):
        super(JobKoreaCrawler, self).__init__()
        self.repeat_count = 10

        self.crawl_url = 'http://www.jobkorea.co.kr/Corp/Person/Find'
        self.read_number = 1

        self.file_link = ''

        self.id = 'dnd8149'
        self.pw = 'dnd8149*'

        self.excel_list = ['URL', '나이', '주소', '학력', '총경력', '경력', '자격증', '어학', '희망근무지', '희망연봉']

    def init_condition(self, crawl_url, read_number=50):

        self.crawl_url = crawl_url
        self.read_number = read_number

    def login_page(self):
        self.url_action('http://www.jobkorea.co.kr/Corp/Main')
        self.wait_action('//*[@id="loginForm"]/div')

        self.input_action('//*[@id="getId"]', self.id)
        self.input_action('//*[@id="getPassword"]', self.pw)

        self.click_action('//*[@id="loginForm"]/div/div[2]/button')

    def set_condition(self):
        self.url_action(self.crawl_url)

        self.wait_action('//*[@id="dvBasicResumeList"]/section/div[1]/div[2]/table')

    def crawling_resume(self):

        count = 0
        current_page = 1

        while True:
            for i in range(0, 30):
                try:
                    people_dict = defaultdict(str)

                    people_dict['URL'] = self.enter_page('//*[@id="dvBasicResumeList"]/section/div[1]'
                                                         '/div[2]/table/tbody/tr[' + str((i % 30) + 1) + ']/td[1]/div[1]/a')

                    self.wait_action('/html/body/div[2]/div/button[1]')
                    self.click_action('/html/body/div[2]/div/button[1]')

                    self.wait_action('/html/body/div[2]/div')

                    people_dict['나이'] = self.get_text('/html/body/div[4]/div[2]/div/div[4]/div[1]/div[2]/div[1]')

                    people_dict['학력'] = self.get_text('/html/body/div[4]/div[2]/div/div[5]/div/div')

                    people_dict['총경력'] = self.get_text('/html/body/div[4]/div[2]/div/div[6]/div[1]/div/div')

                    people_dict['경력'] = self.get_text('/html/body/div[4]/div[2]/div/div[6]/div[2]')

                    people_dict['어학'] = self.get_text('/html/body/div[4]/div[2]/div/div[10]/div')

                    people_dict['자격증'] = self.get_text('/html/body/div[4]/div[2]/div/div[7]/div')

                    people_dict['희망근무조건'] = self.get_text('//*[@id="js-hopeworkAnchor"]/table')

                    for j in self.excel_list:
                        self.csv_data[j].append(people_dict[j])

                    self.go_back_page()

                    self.wait_action('//*[@id="dvBasicResumeList"]/section/div[1]/div[2]/table')

                except Exception as e:
                    print(e)

                count += 1
                self.printProgress(count, self.read_number, 'Progress:', 'Complete', 1, 100)

                if count >= self.read_number:
                    break

            if count >= self.read_number:
                break

            current_page += 1
            self.select_page(str(current_page))

    def make_csv(self):
        df = DataFrame(self.csv_data, columns=self.excel_list)
        file_name = 'csv/JobKorea' + datetime.today().strftime("%Y%m%d%H%M") + '.csv'

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
        self.click_action('//*[@id="dvBasicResumeList"]/section/div[2]/ul/li[' + str(page_number) + ']/a')
        self.wait_action('//*[@id="dvBasicResumeList"]/section/div[1]/div[2]/table')


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
    crawler = JobKoreaCrawler()
    crawler.init_condition('http://www.jobkorea.co.kr/Corp/Person/FindByKey?key=GaxKdhrW75U5eS_kpFGQ0a7dH4ViiwJPqpKJIcryptow22PloLFZy0BPg_aMLOIFjD9tu', 2)
    crawler.run()
