from product import Product
from exception import productNotExist,productAlreadyExist
from pathlib import Path
import pickle
import os
import logging


class DataLoader:

    def __init__(self):
        self.data = {'products': {}, 'id_count': 0}

    def get_product(self, pid):
        if pid not in self.data['products']:
            logging.info(f"Product id not exist: {pid}")
            raise productNotExist(f"Product id not exist: {pid}")
        return self.data['products'][pid]

    def get_products_list(self):
        return self.data['products']

    def add_data(self, name, unit, raw_price, adjunct_price, **specs):
        new_product = Product(name, specs, unit, raw_price, adjunct_price)
        for i in self.data['products'].values():  # todo specs需要处理
            if i == new_product:
                logging.info(f'Product already exists: {i}')
                raise productAlreadyExist(f'Product already exists: {i}')

        logging.info(f'Add product: {new_product}')
        self.data['products'][self.data['id_count']] = new_product
        self.data['id_count'] += 1

    def del_data(self, pid):
        if pid not in self.data['products']:
            logging.info(f"Product id not exist: {pid}")
            raise productNotExist(f"Product id not exist: {pid}")
        else:
            logging.info(f"Delete product id: {pid}, {self.data['products'][pid]}")
            del self.data['products'][pid]

    def save(self, data_dir='data'):
        p = Path(data_dir)
        if not p.exists():
            logging.info(f"Create data directory: {p.resolve}")
            p.mkdir(parents=True)
        p = p/'products.data'
        logging.info(f"Save data: {p.resolve()}")
        with p.open('wb') as f:
            pickle.dump(self.data, f)

    @staticmethod
    def load(data_dir='data'):
        p = Path(data_dir)/'products.data'
        dl = DataLoader()
        if p.exists():
            dl = DataLoader()
            with p.open('rb') as pkl_file:
                dl.data = pickle.load(pkl_file)
            logging.info(f"Load data from file: {p.resolve()}")
            return dl
        else:
            logging.info(f'No existing dir: use empty dataloader')
        return dl

    def __str__(self):
        result = ''
        for i, v in self.data['products'].items():
            result += f'id {i}:{v}\n'
        return result

    def __getitem__(self, item):
        return self.get_product(item)


if __name__ == '__main__':
    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    dl = DataLoader.load()

    # dl.add_data('塑壳断路器', '台', 1220, 130, model='RMM1-630S/3310', current='500A')
    # dl.add_data('塑壳断路器', '台', 1220, 130, model='RMM1-400S/3310', current='350A')
    # dl.del_data(0)
    # dl.add_data('塑壳断路器', '台', 1220, 130, model='RMM1-400S/3310', current='500A')
    print(dl)
    # dl.save()
