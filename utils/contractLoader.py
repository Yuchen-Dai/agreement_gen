from contract import Contract
from pathlib import Path
import datetime
import logging
from excel import Excel
from exception import FileExceed, IllegalContractNumber, ContractNumberAlreadyExist, IllegalDate
import pickle
import re


def _return_information(c):
    return c.supplier, c.buyer, c.brand, (str(c.sign_date.year), str(c.sign_date.month), str(c.sign_date.day)), \
           c.delivery_date, c.delivery_location, c.location, \
           c.payment_method, c.comments, c.others, c.supplier_location, c.supplier_bank, c.supplier_account, \
           c.supplier_tax_num, c.supplier_tel, c.buyer_location, c.buyer_bank, c.buyer_account, c.buyer_tax_num, \
           c.buyer_tel, c.name, c.cid


class ContractLoader:

    def __init__(self, data_dir='data/contract'):
        self.contracts = {}
        self.templates = {}
        self.template_order = []
        self.data_dir = data_dir

        # load contracts
        contracts_path = Path(data_dir) / 'contract'
        if contracts_path.exists():
            for f in contracts_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.contracts[cid] = Contract.load(cid, data_dir)

        # load templates
        template_path = Path(data_dir) / 'template'
        if template_path.exists():
            for f in template_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.templates[cid] = Contract.load(cid, data_dir)

        # load templates' order
        order_path = Path(data_dir) / 'templates.data'
        if order_path.exists():
            with order_path.open('rb') as f:
                self.template_order = pickle.load(f)
        to_be_deleted = []
        for i in range(len(self.template_order)):
            if self.template_order[i] not in self.templates:
                to_be_deleted.append(i)
        to_be_deleted.reverse()
        for i in to_be_deleted:
            del self.template_order[i]
        for cid in self.templates:
            if cid not in self.template_order:
                self.template_order.append(cid)

    def refresh(self):
        """
        Refresh from file.
        :return:
        """
        self.contracts = {}
        self.templates = {}
        self.template_order = []

        # load contracts
        contracts_path = Path(self.data_dir) / 'contract'
        if contracts_path.exists():
            for f in contracts_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.contracts[cid] = Contract.load(cid, self.data_dir)

        # load templates
        template_path = Path(self.data_dir) / 'template'
        if template_path.exists():
            for f in template_path.iterdir():
                cid = f.stem
                if f.suffix == '.data' and isLegalCid(cid):
                    self.templates[cid] = Contract.load(cid, self.data_dir)

        # load templates' order
        order_path = Path(self.data_dir) / 'templates.data'
        if order_path.exists():
            with order_path.open('rb') as f:
                self.template_order = pickle.load(f)
        to_be_deleted = []
        for i in range(len(self.template_order)):
            if self.template_order[i] not in self.templates:
                to_be_deleted.append(i)
        to_be_deleted.reverse()
        for i in to_be_deleted:
            del self.template_order[i]
        for cid in self.templates:
            if cid not in self.template_order:
                self.template_order.append(cid)
        logging.info("Refresh contractloader.")

    def export_excel(self, contract_cid, output_type, file_dir):
        """
        :param contract_cid: Contract
        :param output_type: 1: 合同, 2:报价单
        :param file_dir: The output file
        :return: 1: Fail 0: Success
        """
        e = Excel(self.contracts[contract_cid])
        e.run(output_type=1, file_dir=file_dir)

    def save(self, cid):
        """
        保存指定合同（在基础信息不变，修改了table时,调用此方法）
        :param cid: Contract to be saved
        :return: None
        """
        self.contracts[cid].save(self.data_dir)

    def add_product(self, cid, product, quantity: str, discount: str, comments: str):
        """
        :param cid: Contract to be used
        :param product: Product to be added
        :param quantity: Quantity of product
        :param discount: Discount of product
        :param comments: Comments of product
        :return: 0: Success
                 1: Quantity should be a positive integer.
                 2：Discount should left blank or in format of 0.xxx
                 3: Product already in table
        """
        if not all([i in '0123456789' for i in quantity]) or not quantity:
            return 1
        if not re.match(r"^((0?\.[0-9]+)|1)?$", discount):
            return 2
        if product in [i[0] for i in self.contracts[cid].get_table()]:
            return 3
        if not discount:
            discount = 1
        self.contracts[cid].add_item(product, int(quantity), float(discount), comments)
        return 0

    def remove_product(self, cid, line_number):
        """
        :param cid: Contract to be used
        :param line_number: Line number start from 0
        :return: None
        """
        self.contracts[cid].del_item(line_number)

    def get_table_info(self, cid):
        """
        :param cid: Contract of table
        :return: [(line_num, name, specs, unit, quantity, raw_price, discount, adjunct_price, single_price,
                   total_price, comment)]
        """
        result = []
        for i, (product, quantity, discount, comment) in enumerate(self.contracts[cid].get_table()):
            single_price = product.get_raw_price() * discount + product.get_adjunct_price()
            total_price = single_price * quantity
            result.append((i + 1, product.get_name(), product.get_specs(), product.get_unit(), str(quantity),
                           product.get_raw_price(), str(discount), str(product.get_adjunct_price()),
                           str(single_price), str(total_price), comment))
        return result

    def get_table_total(self, cid):
        """
        :param cid: Contract be used
        :return: total_quantity, total_price
        """
        c = self.contracts[cid]
        return c.get_total_quantity(), c.get_total()

    def get_statistics(self, date):
        """
        :param date: (year, month ,None)
        :return: total of specific date
        """
        year = date[0]
        month = date[1]
        if not year:
            return sum([i.get_total() for i in self.contracts.values()])
        elif not month:
            return sum([i.get_total() for i in self.contracts.values() if i.cid[:2] == year[-2:]])
        else:
            return sum([i.get_total() for i in self.contracts.values() if i.cid[:2] == year[-2:]
                        and i.cid[2:4] == '{:0>2d}'.format(int(month))])

    def get_contract_list(self, date):
        """
        :param date: (year, month ,None)
        :return: [(cid, contract's name)]
        """
        year = date[0]
        month = date[1]
        if not year:
            return list({('00000000', f'20{i[:2]}') for i in self.contracts})
        elif not month:
            return list({('00000000', f'{i[2:4]}') for i in self.contracts if i[:2] == year[-2:]})
        else:
            return [(i, v.get_name()) for i, v in self.contracts.items()
                    if i[:2] == year[-2:] and i[2:4] == '{:0>2d}'.format(int(month))]

    def get_template_list(self):
        """
        :return: [(cid, contract's name)]
        """
        return [(cid, self.templates[cid].get_name()) for cid in self.template_order]

    def override_contract(self, contract_cid, supplier, buyer, brand, sign_date, delivery_date, delivery_location,
                          location, payment_method, comments, others, supplier_location, supplier_bank,
                          supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                          buyer_tax_num, buyer_tel):
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
            c.save(self.data_dir)
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
            c.save(self.data_dir)
        else:
            raise ValueError(f'{contract_cid} not exist.')

    def create_contract(self, supplier, buyer, brand, sign_date, delivery_date, delivery_location,
                        location, payment_method, comments, others, supplier_location, supplier_bank,
                        supplier_account, supplier_tax_num, supplier_tel, buyer_location, buyer_bank, buyer_account,
                        buyer_tax_num, buyer_tel, name, contract_number):
        """
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
        c.set_template(False)
        c.save(self.data_dir)
        self.contracts[c.cid] = c
        logging.info(f"Create contract: {c.cid}")
        return c.cid

    def create_template(self):
        """
        Create a template file
        :return: the cid of new_template.
        """
        c = Contract()
        c.name = "新建模板"
        c.save(self.data_dir)
        self.templates[c.cid] = c
        self.template_order.append(c.cid)
        self._save_template_order()
        logging.info(f"Create template: {c.cid}")
        return c.cid

    def move_template_to_front(self, template_cid):
        """
        :param template_cid: Template to be moved
        :return
        """
        if template_cid in self.template_order:
            self.template_order.remove(template_cid)
            self.template_order.insert(0, template_cid)
            self._save_template_order()

    def get(self, cid):
        """
        :return: All of contract in tuple: supplier, buyer, brand, sign_date, delivery_date, delivery_location,
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
            self.contracts[cid].rename(name)
            self.contracts[cid].save(self.data_dir)
        elif cid in self.templates:
            self.templates[cid].rename(name)
            self.templates[cid].save(self.data_dir)
        else:
            raise ValueError('Cid is not exists.')

    def copy_template(self, template_cid):
        """
        :param template_cid: contract be copied
        :return: cid of new contract
        """
        c = Contract.copy(self.templates[template_cid])
        c.name = self.templates[template_cid].name + '_复制'
        c.save(self.data_dir)
        self.templates[c.cid] = c
        self.template_order.append(c.cid)
        self._save_template_order()
        return c.cid

    def delete(self, cid):
        """
        :param cid: The contract to be deleted
        :return
        """
        if cid in self.contracts:
            self.contracts[cid].delete(self.data_dir)
            del self.contracts[cid]
        elif cid in self.templates:
            self.templates[cid].delete(self.data_dir)
            del self.templates[cid]
            self.template_order.remove(cid)
            self._save_template_order()
        else:
            raise ValueError('Cid is not exists.')

    def generate_contract_num(self, date, last_two=None):
        """
        :param date: (year, month, day)
        :param last_two: last two digits in string format
        :return: Generating number
        """
        try:
            _ = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
        except ValueError:
            raise IllegalDate
        pre_six = '{}{:0>2d}{:0>2d}'.format(str(date[0])[-2:], int(date[1]), int(date[2]))
        if not last_two:
            biggest = 1
            for cid in self.contracts:
                if cid.startswith(pre_six[:4]):
                    this_last_two = int(cid[-2:])
                    if this_last_two >= biggest:
                        biggest = this_last_two + 1
            if biggest > 99:
                raise FileExceed(f'Contracts for this month {pre_six} exceed 100.')
            last_two = '{:0>2d}'.format(biggest)
        else:
            if not all([s in '0123456789' for s in last_two]):
                raise IllegalContractNumber
            last_two = '{:0>2d}'.format(int(last_two))
            if len(last_two) != 2 or last_two == '00':
                raise IllegalContractNumber
            if last_two in [i[-2:] for i in self.contracts if i[:4] == pre_six[:4]]:
                raise ContractNumberAlreadyExist
        return pre_six + last_two

    def _save_template_order(self):
        order_path = Path(self.data_dir) / 'templates.data'
        with order_path.open('wb') as f:
            pickle.dump(self.template_order, f)

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

    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING)
    # for i in range(1,15):
    #     c = Contract(contract_number='210728{:0>2d}'.format(i))
    #     c.set_template(False)
    #     c.save()
    cl = ContractLoader()
    # print(cl.get_template_list())
    # cl.move_template_to_front('00000011')
    # print(cl.get_template_list())
