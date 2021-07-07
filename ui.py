from utils.dataLoader import DataLoader
from utils.excel import Excel
from utils.contract import Contract
import os,logging


def help():
    print('''Not implemented''')


def load(dir):
    dl.load(f'{os.getcwd()}\\{dir}')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING)
    dl = DataLoader()
    dl.load(f'{os.getcwd()}\\data')
    c = Contract(dl)
    while True:
        string = input('请输入指令: ')
        s = string.split()
        command = s[0]
        if command == 'help':
            help()
        elif command == 'load':
            load(s[1])
        else:
            print('Unknown Command.')