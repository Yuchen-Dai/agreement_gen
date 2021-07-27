from contract import Contract
from pathlib import Path
import datetime
from exception import FileExceed, IllegalContractNumber


def _return_information(c):
    return c.supplier, c.buyer, c.brand, (str(c.sign_date.year),str(c.sign_date.month), str(c.sign_date.day)), \
           c.delivery_date, c.delivery_location, c.location, \
           c.payment_method, c.comments, c.others, c.supplier_location, c.supplier_bank, c.supplier_account, \
           c.supplier_tax_num, c.supplier_tel, c.buyer_location, c.buyer_bank, c.buyer_account, c.buyer_tax_num, \
           c.buyer_tel, c.name, c.cid


class ContractLoader:

    def __init__(self, dir='data/contract'):
        self.contracts = {}
        self.templates = {}
        self.dir = dir

        # load contracts
        contracts_path = Path(dir) / 'contract'
        if contracts_path.exists():
            for f in contracts_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.contracts[cid] = Contract.load(cid, dir)

        # load templates
        template_path = Path(dir) / 'template'
        if template_path.exists():
            for f in template_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.templates[cid] = Contract.load(cid, dir)

    def get_contract_list(self):
        """
        :return: [(cid, contract's name)]
        """
        return [(i, v.get_name()) for i, v in self.contracts.items()]

    def get_template_list(self):
        """
        :return: [(cid, contract's name)]
        """
        return [(i, v.get_name()) for i, v in self.templates.items()]

    def override_contract(self, contract_cid, supplier, buyer, brand, sign_date, delivery_date, delivery_location,
                          location, payment_method, comments, others, supplier_location, supplier_bank,
                          supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                          buyer_tax_num, buyer_tel, name, contract_number):
        """
        :param contract_cid: str
        :param supplier: str
        :param buyer: str
        :param brand: str
        :param sign_date: (str,str，str)
        :param delivery_date: str
        :param delivery_location: str
        :param location: str
        :param payment_method: str
        :param comments: str
        :param others: [str]
        :param supplier_location: str
        :param supplier_bank: str
        :param supplier_account: str
        :param supplier_tax_num: str
        :param supplier_tel: str
        :param buyer_location: str
        :param buyer_bank: str
        :param buyer_account: str
        :param buyer_tax_num: str
        :param buyer_tel: str
        :param name: str
        :param contract_number: str
        """
        if contract_cid in self.contracts:
            c = self.contracts[contract_cid]
            c.supplier = supplier
            c.buyer = buyer
            c.brand = brand
            c.update_sign_date(sign_date)
            c.delivery_date = delivery_date
            c.delivery_location = delivery_location
            c.location = location
            c.payment_method = payment_method
            c.comments = comments
            c.others = others
            c.supplier_location = supplier_location
            c.supplier_bank = supplier_bank
            c.supplier_account = supplier_account
            c.supplier_tax_num = supplier_tax_num
            c.supplier_tel = supplier_tel
            c.buyer_location = buyer_location
            c.buyer_bank = buyer_bank
            c.buyer_account = buyer_account
            c.buyer_tax_num = buyer_tax_num
            c.buyer_tel = buyer_tel
            c.name = name
            c.cid = contract_number
            c.save()
        elif contract_cid in self.templates:
            c = self.templates[contract_cid]
            c.supplier = supplier
            c.buyer = buyer
            c.brand = brand
            c.delivery_date = delivery_date
            c.delivery_location = delivery_location
            c.location = location
            c.payment_method = payment_method
            c.comments = comments
            c.others = others
            c.supplier_location = supplier_location
            c.supplier_bank = supplier_bank
            c.supplier_account = supplier_account
            c.supplier_tax_num = supplier_tax_num
            c.supplier_tel = supplier_tel
            c.buyer_location = buyer_location
            c.buyer_bank = buyer_bank
            c.buyer_account = buyer_account
            c.buyer_tax_num = buyer_tax_num
            c.buyer_tel = buyer_tel
            c.name = name
            c.cid = contract_number
            c.save()
        else:
            raise ValueError(f'{contract_cid} not exist.')

    def create_contract(self, contract_cid, supplier, buyer, brand, sign_date, delivery_date, delivery_location,
                        location, payment_method, comments, others, supplier_location, supplier_bank,
                        supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                        buyer_tax_num, buyer_tel, name, contract_number):
        """
        :param contract_cid: str
        :param supplier: str
        :param buyer: str
        :param brand: str
        :param sign_date: (str,str,str)
        :param delivery_date: str
        :param delivery_location: str
        :param location: str
        :param payment_method: str
        :param comments: str
        :param others: [str]
        :param supplier_location: str
        :param supplier_bank: str
        :param supplier_account: str
        :param supplier_tax_num: str
        :param supplier_tel: str
        :param buyer_location: str
        :param buyer_bank: str
        :param buyer_account: str
        :param buyer_tax_num: str
        :param buyer_tel: str
        :param name: str
        :param contract_number: str
        """
        if not isLegalCid(contract_number):
            raise IllegalContractNumber("Not a legal contract number.")
        c = Contract()
        c.contract_cid = contract_cid
        c.supplier = supplier
        c.buyer = buyer
        c.brand = brand
        c.update_sign_date(sign_date)
        c.delivery_date = delivery_date
        c.delivery_location = delivery_location
        c.location = location
        c.payment_method = payment_method
        c.comments = comments
        c.others = others
        c.supplier_location = supplier_location
        c.supplier_bank = supplier_bank
        c.supplier_account = supplier_account
        c.supplier_tax_num = supplier_tax_num
        c.supplier_tel = supplier_tel
        c.buyer_location = buyer_location
        c.buyer_bank = buyer_bank
        c.buyer_account = buyer_account
        c.buyer_tax_num = buyer_tax_num
        c.buyer_tel = buyer_tel
        c.name = name
        c.cid = contract_number
        c.save()
        self.contracts[c.cid] = c

    def create_template(self):
        """
        Create a template file
        :return the cid of new_template.
        """
        c = Contract()
        c.save(self.dir)
        self.templates[c.cid] = c
        return c.cid

    def get_contract(self, cid):
        """
        :return  All of contract in tuple: supplier, buyer, brand, sign_date, delivery_date, delivery_location,
                          location, payment_method, comments, others, supplier_location, supplier_bank,
                          supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                          buyer_tax_num, buyer_tel, name, contract_number
        """
        if cid in self.contracts:
            return _return_information(self.contracts[cid])
        elif cid in self.templates:
            return _return_information(self.templates[cid])
        else:
            raise ValueError('Cid is not exists.')

    def rename(self, cid: str, name: str):
        """
        :param cid: The contract to be renamed
        :param name: New name
        :return:
        """
        if cid in self.contracts:
            self.contracts[cid].name = name
        elif cid in self.templates:
            self.templates[cid].name = name
        else:
            raise ValueError('Cid is not exists.')

    def delete(self, cid):
        """
        :param cid: The contract to be deleted
        :return:
        """
        if cid in self.contracts:
            self.contracts[cid].delete(self.dir)
            del self.contracts[cid]
        elif cid in self.templates:
            self.templates[cid].delete(self.dir)
            del self.templates[cid]
        else:
            raise ValueError('Cid is not exists.')

    @staticmethod
    def generate_contract_num(date, dir='data/contract'):
        """ in: date: (year, month, day)
            out: eight digits string
        """
        p = Path(dir) / 'contract'
        pre_six = '{}{:0>2d}{:0>2d}'.format(str(date[0])[-2:], int(date[1]), int(date[2]))
        if not p.exists():
            return pre_six + '01'
        check_occupy = [True] * 99
        for i in p.iterdir():
            if i.stem.startswith(pre_six[:4]):
                check_occupy[int(i.stem[6:8]) - 1] = False
        last_two = None
        for i, not_occupy in enumerate(check_occupy):
            if not_occupy:
                last_two = i + 1
                break
        if not last_two:
            raise FileExceed(f'Contract for {pre_six} exceed 100.')
        return '{}{:0>2d}'.format(pre_six, last_two)

    @staticmethod
    def get_today():
        """ Get today's date: (year, month, day)"""
        today = datetime.date.today()
        return str(today.year), str(today.month), str(today.day)


def isLegalCid(cid):
    if type(cid) != str:
        return False
    if len(cid) != 8:
        return False
    if not cid[:8].isnumeric():
        return False
    if cid.startswith('0000'):
        return True
    try:
        datetime.datetime(2000 + int(cid[:2]), int(cid[2:4]), int(cid[4:6]))
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    import os
    import logging

    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING)
    cl = ContractLoader()

