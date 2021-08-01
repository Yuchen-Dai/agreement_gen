from main_window import MainWindow
from dataLoader import DataLoader
from contractLoader import ContractLoader

dl = DataLoader.load()
cl = ContractLoader()
main_window = MainWindow(dl, cl)
