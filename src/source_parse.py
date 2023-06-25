import time

import requests

from src.filter_date import FilterDate


class GetLinksShape:
    def __init__(self, filter_count_day=1):

        self.filter_count_day = filter_count_day

        self.old_date = ''

    def get_data_page(self):

        data_good_list = []

        count_page = 0

        while True:

            headers = {
                'authority': 'api.prod.grantshares.io',
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                # 'cookie': '_ga=GA1.1.3086494.1687698669; _ga_L1GFSYJLPT=GS1.1.1687698668.1.1.1687698917.0.0.0',
                'origin': 'https://grantshares.io',
                'referer': 'https://grantshares.io/',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }

            params = {
                'page': f'{count_page}',
                'page-size': '25',
                'order-attr': 'state-updated',
                'order-asc': '0',
            }

            response = requests.get('https://api.prod.grantshares.io/api/proposal/all', params=params, headers=headers)

            res = response.json()

            data_good_list.extend(res['items'])

            data_iter_stop = FilterDate.check_data(
                data_good_list[-1]['offchain_creation_timestamp'], self.filter_count_day)

            if self.old_date == data_iter_stop:
                """Что бы бесконечно не собирал"""

                return data_good_list

            if not data_iter_stop:
                return data_good_list

            self.old_date = data_iter_stop

            time.sleep(2)

        return data_good_list


if __name__ == '__main__':
    data_dict = GetLinksShape(1).get_data_page()

    print()
