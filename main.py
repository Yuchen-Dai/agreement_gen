from main_window import MainWindow
from dataLoader import DataLoader
from contractLoader import ContractLoader
from quoteLoader import QuoteLoader
from setting_window import SettingWindow
import logging

logging_dict = {'0': logging.DEBUG, '1': logging.INFO, '2': logging.WARNING, '3': logging.ERROR,
                '4': logging.FATAL}
SettingWindow.load_setting()
settings = SettingWindow.settings
logging_level = logging_dict[settings['logging_level']]
logging.basicConfig(filename='logger.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging_level)
dl = DataLoader.load()
cl = ContractLoader()
ql = QuoteLoader()
main_window = MainWindow(dl, cl, ql)
