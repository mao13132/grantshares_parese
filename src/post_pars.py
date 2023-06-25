import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.get_comments import GetComments


class PostPars:
    def __init__(self, driver, data_post):
        self.driver = driver
        self.source_name = 'grantshares'
        self.data_post = data_post

    def load_page(self, url):
        try:

            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на "{url}" "{es}"')
            return False

    def __check_load_page(self, name_post):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
            return False

    def loop_load_page(self, post):
        coun = 0
        coun_ower = 10

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name_post"]}')
                return False

            response = self.load_page(post['link'])

            if not response:
                continue

            result_load = self.__check_load_page(post['name_post'])

            if not result_load:
                self.driver.refresh()
                return False

            return True

    def get_step_voitting(self):
        try:
            step = step = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'timeline_container')]"
                                                                      f"//*[contains(@class, 'is-current')]"
                                                                      f"//parent::div/h4").text


        except:
            step = ''

        return step

    def get_text_post(self):
        try:
            text_post = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'preview_content')]").text


        except:
            text_post = ''

        return text_post

    def get_name_author(self):
        try:
            name_author = self.driver.find_element(by=By.XPATH, value=f"//td[contains(@class, 'lead')]").text


        except:
            name_author = ''

        return name_author

    def get_voting_starts(self):
        try:
            voting_starts = self.driver.find_element(by=By.XPATH,
                                                     value=f"//*[contains(text(), 'Voting starts')]//parent::tr").text
        except:
            voting_starts = ''

        try:
            voting_starts = voting_starts.split('\n')[-1]
        except:
            voting_starts = ''

        return voting_starts

    def get_voting_end(self):
        try:
            voting_end = self.driver.find_element(by=By.XPATH,
                                                  value=f"//*[contains(text(), 'Voting ends')]//parent::tr").text
        except:
            voting_end = ''

        try:
            voting_end = voting_end.split('\n')[-1]
        except:
            voting_end = ''

        return voting_end

    def get_funding(self):
        try:
            funding = self.driver.find_elements(by=By.XPATH, value=f""
                                                                   f"//*[contains(text(), 'Token Amount')]"
                                                                   f"//parent::tr/td")[-1].text
        except:
            funding = ''

        try:
            funding = funding.split('\n')[-1]
        except:
            funding = ''

        return funding

    def get_voting_yes(self):
        try:
            voting_yes = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'voting-status')]"
                                                                     f"//div[contains(@class, 'yes')]").text


        except:
            voting_yes = ''

        return voting_yes

    def get_voting_no(self):
        try:
            voting_no = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'voting-status')]"
                                                                    f"//div[contains(@class, 'no')]").text


        except:
            voting_no = ''

        return voting_no

    def get_voting_abstain(self):
        try:
            voting_abstain = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'voting-status')]"
                                                                         f"//div[contains(@class, 'abstain')]").text


        except:
            voting_abstain = ''

        return voting_abstain

    def start_pars(self):
        for count, post in enumerate(self.data_post):

            result_load_page = self.loop_load_page(post)

            if not result_load_page:
                continue

            post['step'] = self.get_step_voitting()
            post['text_post'] = self.get_text_post()
            post['name_author'] = self.get_name_author()
            post['voting_starts'] = self.get_voting_starts()
            post['voting_end'] = self.get_voting_end()
            post['get_funding'] = self.get_funding()
            post['voting_yes'] = self.get_voting_yes()
            post['voting_no'] = self.get_voting_no()
            post['voting_abstain'] = self.get_voting_abstain()

            list_comments = GetComments(self.driver).start(post)


        return self.data_post


if __name__ == '__main__':
    from browser.createbrowser import CreatBrowser
    from src.temp import good_list

    browser_core = CreatBrowser()

    ower_good_data = PostPars(browser_core.driver, good_list).start_pars()

    print()
