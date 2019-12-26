from auth2 import Auth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AccountInfo(Auth):
    __wait_ = None

    def __init__(self, login_, pass_, silent_=True):
        super().__init__(login_, pass_, silent_)
        super().run_auth_lf()
        self.__wait_ = WebDriverWait(super().get_driver(), super().TIME_WAIT)

    @staticmethod
    def is_watch_episode(class_: str):
        l = class_.split(' ')

        if 'checked' in l:
            return True

        return False

    def get_serial_info(self, serial_name: str) -> list:
        """
        :param serial_name:
        :return:
        """
        super().open_page('series/' + serial_name + '/seasons/')

        seasons = self.__wait_.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.serie-block')),
            'Error, `serie-block` not found!')

        _l = list()

        for season in seasons:
            _s = {
                's_name': season.find_element_by_css_selector('h2').text,
                's_picture': season.find_element_by_css_selector('.movie-cover-box .cover').get_attribute('src'),
                's_detail': str(season.find_element_by_css_selector('.details').text).split('\n'),
                'episodes': list()
            }

            episodes = season.find_elements_by_css_selector('.movie-parts-list tr')

            _ep = None

            for episode in episodes:
                _ep = {
                    'e_num': episode.find_element_by_css_selector('td.beta').text,
                    'e_name': str(episode.find_element_by_css_selector('td.gamma').text).split('\n'),
                    'e_release': str(episode.find_element_by_css_selector('td.delta').text).split('\n'),
                    'e_rank': episode.find_element_by_css_selector('td.epsilon .mark-green-box').text,
                    'e_status': self.is_watch_episode(
                        episode.find_element_by_css_selector('.haveseen-btn').get_attribute('class'))
                }

                _s['episodes'].append(_ep)

                _l.append(_s)

        return _l

    def get_all_link_to_my_serials(self) -> list:
        super().open_page('my')

        serials_list = self.__wait_.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.serial-box')),
            'Error, `serial-box` not found !')

        links = [box.find_element_by_css_selector('.body').get_attribute('href') for box in serials_list]

        return links

    def get_statistics(self) -> dict:
        """
        :return:
        total_e total watching series
        total_h total watching in hours
        total_d total watching in days
        """
        super().open_page('my')

        profile_stat = self.__wait_.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.profile-stat .charts-box div > div > span')),
            'Error find `get_statistics` !')

        _s = [_e.text if _e.text else '--' for _e in profile_stat]

        s = {'total_e': _s[0], 'total_h': _s[1], 'total_d': _s[2]}

        return s


if __name__ == '__main__':
    account = None
    try:
        account = AccountInfo('login', 'password')
        # print(account.get_statistics())
        # account.get_all_link_to_my_serials()
        res = account.get_serial_info('Supernatural')

        print(res[0])

    finally:
        if account:
            account.close_driver()
