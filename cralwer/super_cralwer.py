from cralwer.super_selenium import SuperSelenium
import sys

# 상속 해주는 크롤링 클래스
class SuperCrawler(SuperSelenium):
    def __init__(self):
        super(SuperCrawler, self).__init__()

    def run(self):
        self.load_page()
        self.set_condition()
        self.crawling_resume()
        self.make_csv()
        # self.driver.quit()

    def load_page(self):
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






