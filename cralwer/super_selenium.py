from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


class SuperSelenium(object):
    def __init__(self):
        print('시작')
        self.driver = webdriver.Chrome()

    def url_action(self, url):
        self.driver.get(url)

    def new_tab_url_action(self, url):
        self.driver.get(url)

    def click_action(self, xpath):
        for i in range(0, 10):
            try:
                button = self.find_element(xpath)
                button.click()
            except Exception as e:
                print(e)
                continue
            break

    def click_open_tab_action(self, xpath):
        self.driver.find_element_by_xpath(xpath).send_keys(Keys.CONTROL + Keys.SHIFT)
        for i in range(0, 10):
            try:
                # button = self.find_element(xpath)

                # button.click()
                pass
            except Exception as e:
                print(e)
                continue
            break

    def wait_action(self, xpath):
        delay = 3
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

            return True
        except TimeoutException:
            return False

    def long_wait_action(self, xpath):
        delay = 15
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

            return True
        except TimeoutException:
            return False

    def input_action(self, xpath, keyword):
        input_field = self.find_element(xpath)
        input_field.send_keys(keyword)

    def clear_action(self, xpath):
        clear_filed = self.find_element(xpath)
        clear_filed.clear()

    def find_element(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)

        return element

    def find_elements(self, xpath):
        elements = self.driver.find_elements_by_xpath(xpath)

        return elements

    def get_text(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)

        return element.text

    def wait_time_action(self, delay):
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'a')))
        except TimeoutException:
            pass

    def go_back_page(self):
        self.driver.execute_script("window.history.go(-1)")

    def open_page(self, url):
        self.driver.navigate().to(url)

    def check_alert(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Timed out waiting for PA creation ' +
                                                'confirmation popup to appear.')

            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except TimeoutException:
            return False
