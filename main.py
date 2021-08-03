from main_window import MainWindow
from dataLoader import DataLoader
from contractLoader import ContractLoader
from pathlib import Path
import logging

logging_dict = {'0': logging.DEBUG, '1': logging.INFO, '2': logging.WARNING, '3': logging.ERROR,
                '4': logging.FATAL}
setting_path = Path('setting.yaml')
settings = {}
if setting_path.exists():
    with setting_path.open('r') as f:
        for line in f.readlines():
            setting = line.strip().split(':')
            settings[setting[0]] = setting[1]
if 'logging_level' in settings:
    logging_level = logging_dict[settings['logging_level']]
else:
    logging_level = logging.WARNING
logging.basicConfig(filename='logger.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging_level)

dl = DataLoader.load()
cl = ContractLoader()
main_window = MainWindow(dl, cl)
