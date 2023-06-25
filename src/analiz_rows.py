import base64
import json

from src.filter_date import FilterDate


class AnalizRows:
    def __init__(self, dict_rows, filter_count_day):
        self.dict_rows = dict_rows
        self.filter_count_day = filter_count_day

    def decoder_title(self, title_base64):
        try:

            base64_bytes = title_base64.encode("ascii")

            sample_string_bytes = base64.b64decode(base64_bytes)

            sample_string = sample_string_bytes.decode("ascii")

        except Exception as es:

            print(f'Ошибка при декодирование имени "{es}"')

            sample_string = ''

        return sample_string

    def start_iter(self):

        good_list = []

        for count, post in enumerate(self.dict_rows):

            chech_date = FilterDate.check_data(post['offchain_creation_timestamp'], self.filter_count_day)

            if not chech_date:
                continue

            good_itter = {}

            good_itter['id'] = post['offchain_id']
            good_itter['name_post'] = self.decoder_title(post['title'])
            good_itter['date_post'] = chech_date.strftime('%d.%m.%y')
            good_itter['link'] = 'https://grantshares.io/app/details/' + post['offchain_id']
            good_itter['link_git'] = post['discussion_url']
            good_itter['name_them'] = post['type']
            good_list.append(good_itter)

        return good_list



if __name__ == '__main__':
    from src.temp import *

    filter_count_day = 60

    data_ads_row = AnalizRows(data_row, filter_count_day).start_iter()

    print()
