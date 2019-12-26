from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class Auth:
    __driver = None
    __options = None
    __login_ = None
    __pass_ = None

    SITE = 'https://www.lostfilm.tv/'
    TIME_WAIT = 60

    def __init__(self, login_, pass_, silent_=True):
        self.__options = webdriver.FirefoxOptions()
        self.__options.headless = silent_  # set silent mode

        self.__login_ = login_
        self.__pass_ = pass_

    def open_page(self, path):
        self.__driver.get(self.SITE + path)
        pass

    def get_driver(self):
        return self.__driver

    def close_driver(self):
        self.__driver.quit()
        pass

    def run_auth_lf(self):
        try:
            self.__driver = webdriver.Firefox(executable_path='geckodriver.exe', options=self.__options)
            self.open_page("auth/gp/?t=1")

            wait = WebDriverWait(self.__driver, self.TIME_WAIT)

            wait.until(EC.title_is('Вход – Google Аккаунты'),
                               'Title \'Вход – Google Аккаунты\' not found!')  # Wait load page accounts.google.com

            email_field = wait.until(EC.visibility_of_element_located((By.ID, 'identifierId')),
                                             'Element id=\'identifierId\' not found!')  # Wait load email field

            email_field.send_keys(self.__login_)  # Fill email filed

            sleep(2)

            email_field.send_keys(Keys.ENTER)

            pass_field = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')),
                'Element \'input[name="password"]\' not found!')  # Wait load pass field

            pass_field.send_keys(self.__pass_)  # Fill pass filed

            sleep(2)

            pass_field.send_keys(Keys.ENTER)

            wait.until(EC.url_to_be(self.SITE), 'Error load lostfilm.tv page!')
        except Exception as er:
            print(er)
            self.close_driver()
        else:
            return True


if __name__ == '__main__':
    pass
