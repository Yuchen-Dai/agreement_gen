from excel import Excel
import re


class QuoteLoader:
    def __init__(self, data_dir='data/quotes'):
        self.quotes = {}
        self.data_dir = data_dir

        # load quotes
        pass

    def refresh(self):
        pass

    def export_excel(self, qid, output_type, file_dir):
        """
        :param qid: quote to be export
        :param output_type: 1: 合同, 2:报价单
        :param file_dir: The output file
        :return: 1: Fail 0: Success
        """
        e = Excel(self.quotes[qid])
        e.run(output_type=2, file_dir=file_dir)

    def save_quote(self, qid):
        """
        在基础信息不变，修改了table时,调用此方法
        :param qid: Quote to be saved
        :return: None
        """
        self.quotes[qid].save()

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
        pass  # todo

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
        :return:
        """
        pass

    def overrider_quote(self, project_name, date, buyer_name, buyer_contact, buyer_tel,
                     quote_contact, quote_tel, qq):
        """
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
        pass

    def get_quote(self, qid):
        """
        :param qid:
        :return: project_name, date, buyer_name, buyer_contact, buyer_tel,
                     quote_contact, quote_tel, qq
        """
        pass
        return '',('','',''),'','','','','','',''

    def rename(self, qid, name):
        """
        :param qid:
        :param name:
        :return:
        """
        pass

    def del_quote(self, qid):
        """
        :param qid:
        :return:
        """
        pass

    @staticmethod
    def get_today():
        """ Get today's date: (year, month, day)"""
        today = datetime.date.today()
        return str(today.year), str(today.month), str(today.day)