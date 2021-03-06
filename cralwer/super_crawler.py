from cralwer.super_selenium import SuperSelenium
import sys
from collections import defaultdict


# 상속 해주는 크롤링 클래스
class SuperCrawler(SuperSelenium):
    def __init__(self):
        super(SuperCrawler, self).__init__()
        self.csv_data = defaultdict(list)

    def run(self):
        self.login_page()
        self.set_condition()
        self.crawling_resume()
        self.make_csv()
        self.driver.quit()

    def login_page(self):
        raise NotImplementedError

    def set_condition(self):
        raise NotImplementedError

    def crawling_resume(self):
        raise NotImplementedError

    def make_csv(self):
        raise NotImplementedError

    def printProgress(self, iteration, total, prefix='', suffix='', decimals=1, barLength=100):
        formatStr = "{0:." + str(decimals) + "f}"

        percent = formatStr.format(100 * (iteration / float(total)))
        filledLength = int(round(barLength * iteration / float(total)))
        bar = '#' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),

        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()






