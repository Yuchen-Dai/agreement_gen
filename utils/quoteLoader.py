from excel import Excel
from quote import Quote
from pathlib import Path
import re
import datetime
import logging



class QuoteLoader:
    def __init__(self, data_dir='data'):
        self.quotes = {}
        self.data_dir = data_dir

        # load quotes
        quotes_path = Path(self.data_dir) / 'quote'

        if quotes_path.exists():
            for f in quotes_path.iterdir():
                qid = f.stem
                if f.suffix == '.data':
                    self.quotes[qid] = Quote.load(qid, self.data_dir)

    def refresh(self):
        self.quotes = {}
        quotes_path = Path(self.data_dir) / 'quote'
        if quotes_path.exists():
            for f in quotes_path.iterdir():
                qid = f.stem
                if f.suffix == '.data':
                    self.quotes[qid] = Quote.load(qid, self.data_dir)

    def export_excel(self, qid, output_type, file_dir):
        """
        :param qid: quote to be export
        :param output_type: 1: 合同, 2:报价单
        :param file_dir: The output file
        :return: 1: Fail 0: Success
        """
        e = Excel(self.quotes[qid])
        e.run(output_type=2, file_dir=file_dir)

    def save(self, qid):
        """
        在基础信息不变，修改了table时,调用此方法
        :param qid: Quote to be saved
        :return: None
        """
        self.quotes[qid].save(self.data_dir)

    def add_product(self, qid, product, quantity: str, discount: str, comments: str):
        """
        :param qid: Contract to be used
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
        if product in [i[0] for i in self.quotes[qid].get_table()]:
            return 3
        if not discount:
            discount = 1
        self.quotes[qid].add_item(product, int(quantity), float(discount), comments)
        return 0

    def remove_product(self, qid, line_number):
        """
        :param qid: Contract to be used
        :param line_number: Line number start from 0
        :return: None
        """
        self.quotes[qid].del_item(line_number)

    def get_table_info(self, qid):
        """
        :param qid: Contract of table
        :return: [(line_num, name, specs, unit, quantity, raw_price, discount, adjunct_price, single_price,
                   total_price, comment)]
        """
        result = []
        for i, (product, quantity, discount, comment) in enumerate(self.quotes[qid].get_table()):
            single_price = product.get_raw_price() * discount + product.get_adjunct_price()
            total_price = single_price * quantity
            result.append((i + 1, product.get_name(), product.get_specs(), product.get_unit(), str(quantity),
                           product.get_raw_price(), str(discount), str(product.get_adjunct_price()),
                           str(single_price), str(total_price), comment))
        return result

    def get_table_total(self, qid):
        """
        :param qid: Contract be used
        :return: total_quantity, total_price
        """
        q = self.quotes[qid]
        return q.get_total_quantity(), q.get_total()

    def get_quote_list(self, date):
        """
        :param date: (year, month ,None)
        :return: [(qid, quote's name)]
        """
        year = date[0]
        month = date[1]
        if not year:
            return list({('00000000', f'20{i[:2]}') for i in self.quotes})
        elif not month:
            return list({('00000000', f'{i[2:4]}') for i in self.quotes if i[:2] == year[-2:]})
        else:
            return [(i, v.get_name()) for i, v in self.quotes.items()
                    if i[:2] == year[-2:] and i[2:4] == '{:0>2d}'.format(int(month))]

    def create_quote(self, project_name, date, buyer_name, buyer_contact, buyer_tel,
                     quote_contact, quote_tel, qq, name):
        """
        :param project_name:
        :param date: (year, month, day)
        :param buyer_name:
        :param buyer_contact:
        :param buyer_tel:
        :param quote_contact:
        :param quote_tel:
        :param qq:
        :param name:
        :return: (year, month, None), qid
        """
        q = Quote(project_name=project_name, date=date, buyer_name=buyer_name, buyer_contact=buyer_contact,
                  buyer_tel=buyer_tel, quote_contact=quote_contact, quote_tel=quote_tel, qq=qq, name=name)
        q.save(self.data_dir)
        qid = q.get_qid()
        self.quotes[qid] = q
        logging.info(f"Create contract: {qid}")
        return (f'20{qid[:2]}', qid[2:4], None), qid

    def override_quote(self, qid, project_name, date, buyer_name, buyer_contact, buyer_tel,
                        quote_contact, quote_tel, qq):
        """
        :param qid:
        :param project_name:
        :param date: (year, month, day)
        :param buyer_name:
        :param buyer_contact:
        :param buyer_tel:
        :param quote_contact:
        :param quote_tel:
        :param qq:
        :return:
        """
        if qid in self.quotes:
            q = self.quotes[qid]
            q.project_name = project_name
            q.set_date(date)
            q.buyer_name = buyer_name
            q.buyer_contact = buyer_contact
            q.buyer_tel = buyer_tel
            q.quote_contact = quote_contact
            q.quote_tel = quote_tel
            q.qq = qq
            q.save(self.data_dir)

    def get(self, qid):
        """
        :param qid:
        :return: project_name, date, buyer_name, buyer_contact, buyer_tel,
                     quote_contact, quote_tel, qq, name, qid
        """
        if qid in self.quotes:
            q = self.quotes[qid]
            return q.project_name, q.get_date(), q.buyer_name, q.buyer_contact, q.buyer_tel, \
                   q.quote_contact, q.quote_tel, q.qq, q.name, qid

    def rename(self, qid, name):
        """
        :param qid:
        :param name:
        :return:
        """
        if qid in self.quotes:
            self.quotes[qid].rename(name)
            self.quotes[qid].save(self.data_dir)

    def delete(self, qid):
        """
        :param qid:
        :return:
        """
        if qid in self.quotes:
            self.quotes[qid].delete(self.data_dir)
            del self.quotes[qid]

    @staticmethod
    def get_today():
        """ Get today's date: (year, month, day)"""
        today = datetime.date.today()
        return str(today.year), str(today.month), str(today.day)


if __name__ == '__main__':
    import os
    os.chdir('../')
    ql = QuoteLoader()
    a = ql.get_quote_list(('2021','08',None))
    print(a)
