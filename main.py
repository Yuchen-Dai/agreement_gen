from main_window import MainWindow
from dataLoader import DataLoader


dl = DataLoader.load()
main_window = MainWindow(dl)
