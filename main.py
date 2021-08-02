from main_window import MainWindow
from dataLoader import DataLoader
from contractLoader import ContractLoader
import logging

logging.basicConfig(filename='logger.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.ERROR)
dl = DataLoader.load()
cl = ContractLoader()
main_window = MainWindow(dl, cl)
