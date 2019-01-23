from cralwer.super_crawler import SuperCrawler
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pandas import DataFrame
from collections import defaultdict


class WorknetCrawler(SuperCrawler):
    def __init__(self):
        super(WorknetCrawler, self).__init__()
        self.repeat_count = 10

        self.crawl_url = 'https://www.work.go.kr/psnInfo/psnInfoSrch/dtlPsnSrch.do'
        self.read_number = 1

        self.file_link = ''

        self.id = 'dnd8149'
        self.pw = 'dandd8149*'

        self.excel_list = ['URL', '경력', '희망급여', '출생연도', '주소', '학력사항', '희망직종', '경력사항', '주요업무', '자격증', '컴퓨터활용']

    def init_condition(self, crawl_url, read_number=50):
        self.crawl_url = crawl_url
        self.read_number = read_number

    def login_page(self):
        self.url_action('https://www.work.go.kr/member/bodyLogin.do')
        self.wait_action('//*[@id="loginArea"]/div[2]')

        self.driver.switch_to_window(self.driver.window_handles[0])

        self.input_action('//*[@id="custId2"]', self.id)
        self.input_action('//*[@id="pwd2"]', self.pw)

        self.click_action('//*[@id="loginArea"]/div[2]/div[1]/button')

        self.wait_action('//*[@id="wrapper"]/div/div/div[2]/button[1]')
        self.click_action('//*[@id="wrapper"]/div/div/div[2]/button[1]')

    def set_condition(self):
        self.url_action(self.crawl_url)
        self.wait_action('//*[@id="subInfoForm"]/div[2]')

    def crawling_resume(self):
        count = 0
        current_page = 1

        while True:
            for i in range(0, 10):
                try:
                    people_dict = defaultdict(str)

                    people_dict['URL'] = self.enter_page('//*[@id="subInfoForm"]/div[2]/table/tbody/tr['
                                                         + str((count % 10) + 1) + ']/td[1]/div/a')

                    if self.check_alert():
                        count += 1
                        self.read_number += 1
                        continue

                    self.wait_action('//*[@id="contents"]/div[2]')

                    people_dict['총경력'] = self.get_text('//*[@id="contents"]/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/span')

                    people_dict['희망직종'] = self.get_text('//*[@id="Table8"]/tbody/tr[5]/td/table/tbody'
                                                                 '/tr/td[4]/table/tbody/tr/td/table/tbody/tr[4]/'
                                                                 'td/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td[4]')

                    people_dict['희망연봉'] = self.get_text('//*[@id="contents"]/div[2]/div[2]/div[2]/div[1]/div/ul/li[3]/span')

                    people_dict['출생연도'] = self.get_text('//*[@id="contents"]/div[2]/div[2]/div[2]/div[2]/div/ul/li[4]/span')

                    people_dict['출생연도'] = people_dict['출생연도'].replace(' ', '')

                    people_dict['주소'] = self.get_text('//*[@id="contents"]/div[2]/div[2]/div[2]/div[2]/div/ul/li[2]/span')

                    people_dict['주소'] = people_dict['주소'].replace(' ', '')

                    people_dict['학력사항'] = self.get_text('//*[@id="contents"]/div[2]/div[3]/table/tbody')

                    people_dict['희망직종'] = self.get_text('//*[@id="contents"]/div[2]/div[4]/table/tbody')

                    people_dict['경력사항'] = self.get_text('//*[@id="contents"]/div[2]/div[6]/table')

                    people_dict['주요업무'] = self.get_text('//*[@id="contents"]/div[2]/div[7]/table')

                    people_dict['자격증'] = self.get_text('//*[@id="contents"]/div[2]/div[21]/table/tbody')

                    people_dict['컴퓨터활용'] = self.get_text('//*[@id="contents"]/div[2]/div[22]/table/tbody/tr/td')

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

        file_name = 'csv/WorkNet' + datetime.today().strftime("%Y%m%d%H%M") + '.csv'

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
        self.click_action('//*[@id="subInfoForm"]/nav/a[' + str(page_number + 1) + ']')
        self.wait_action('//*[@id="subInfoForm"]/div[2]')

    def enter_page(self, xpath):
        button = self.find_element(xpath)

        link_url = button.get_property('href')
        self.url_action(link_url)

        return link_url


if __name__ == '__main__':
    crawler = WorknetCrawler()
    crawler.init_condition('https://www.work.go.kr/psnInfo/psnInfoSrch/dtlPsnSrch.do?carOwnerYn=&careerTo=&'
                           'militaryExcHopeCd=&occupation=01&rot2WorkYn=&payGbn=&resultCnt=10&birthFromYY=&'
                           'cert=&minPay=&hopePl=&searchOn=Y&careerTypes=&subEmpHopeYn=&academicGbn=&foriegn'
                           '=%2C%2C&isChkLocCall=&major=&maxage=&minage=&foriegnYn=%2C%2C&sortField=DATE&moerButt'
                           'onYn=&drivePossibleYn=&sortOrderBy=DESC&keyword=&birthToYY=&academicGbnoEdu=Y&termSear'
                           'chGbn=all&sexCd=N&webIsOut=&isEmptyHeader=&maxPay=&_csrf=b2896595-eb82-41c9-b099-7024189b5'
                           '854&readjustPossYn=&pageCode=&rot3WorkYn=&regDateEndt=&pageIndex=1&careerFrom=&computerCd=&emp'
                           'loyGbn=&disableYn=&region=&regDateStdt=#viewSPL', 2)
    crawler.run()
