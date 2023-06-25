from datetime import datetime

from browser.createbrowser import CreatBrowser
from save_result import SaveResult
from src.analiz_rows import AnalizRows
from src.post_pars import PostPars
from src.source_parse import GetLinksShape


class ShapeshiftPostParser:
    pass


def main():
    filter_count_day = 60

    print(f'Парсер запущен. Получаю данные')
    
    response_data = GetLinksShape(filter_count_day).get_data_page()

    good_list = AnalizRows(response_data, filter_count_day).start_iter()

    print(f'Собрал {len(good_list)} подходящий поста (ов) с фильтром {filter_count_day}')

    browser_core = CreatBrowser()

    ower_good_data = PostPars(browser_core.driver, good_list).start_pars()

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResult(ower_good_data).save_file(file_name)



if __name__ == '__main__':
    main()

    print(f'Работу закончил')
