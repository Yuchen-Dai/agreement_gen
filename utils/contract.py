import logging
import os
import time

from dataLoader import DataLoader
from exception import productNotExist


class Contract:
    def __init__(self, dl, buyer, location,date = None, supplier='广州市森源电气有限公司'):
        self.products = dl.get_products()
        self.location = location
        self.supplier = supplier
        self.buyer = buyer
        self.date = date
        self.table = []  # [(product_id, quantity, discount)]

    def add_item(self, product_id, quantity, discount=1):
        if product_id not in self.products:
            logging.info(f"Product id not exist: {product_id}")
            raise productNotExist(f"Product id not exist: {product_id}")
        self.table.append((product_id, quantity, discount))

    def del_item(self, line_number):
        logging.info(f"Del line: {line_number}")
        del self.table[line_number]

    def get_date(self):
        if not self.date:
            return time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        else:
            return self.date

    def get_product(self, product_id):
        if product_id not in self.products:
            logging.info(f"Product id not exist: {product_id}")
            raise productNotExist(f"Product id not exist: {product_id}")
        return self.products[product_id]

    def display_table(self):
        for i, line in enumerate(self.table):
            print(i, self.products[line[0]], 'quantity:', line[1], 'discount:', line[2])

    def get_contract_num(self):
        pass # todo
        return '21051425'

    def get_location(self):
        return self.location

    def get_buyer(self):
        return self.buyer

    def get_supplier(self):
        return self.supplier

    def get_total(self):
        total = 0
        for line in self.table:
            p = self.products[line[0]]
            total += line[1] * (p.get_raw_price() * line[2] + p.get_adjunct_price())
        return total

    def get_total_daxie(self):
        return numToBig(self.get_total())

    def get_brand(self):
        yield '上海人民', self.get_total()  # todo

    def get_payment_method(self):
        pass # todo
        return '发货前需方支付100%货款给供方。'

    def get_supplementary(self):
        pass # todo
        return ''

    def get_jiaohuo(self):
        pass # todo
        return f'合同生效后10个工作日货到{self.location}。'

    def get_table(self):
        return self.table

    def load(self, dir):
        pass # todo


    def save(self, dir):
        pass # todo


def numToBig(num):
    dict1 = {1: '壹', 2: '贰', 3: '叁', 4: '肆', 5: '伍', 6: '陆', 7: '柒', 8: '捌', 9: '玖', 0: '零'}
    dict2 = {2: '拾', 3: '佰', 4: '仟', 5: '万', 6: '拾', 7: '佰', 8: '仟', 1: '元', 9: '角', 10: '分', 11: '整'}
    money = ''  # 最终大写数字
    flag = False  # 去掉多余的十百千
    flag2 = False  # 增加零
    ifint = False  # 整
    count = 0
    count2 = 8
    if int(num) == num:
        num = int(num)
    strnum = str(num)

    aa = strnum.split('.')
    bb = list(str(aa[:1])[2:-2])
    cc = list(str(aa[1:])[2:-2])
    # 此处控制：无小数时输出xxx元整
    # 若要求一位小数也带整，即xxx元整并且xxx元xx角整，则修改下方0为1
    if len(cc) <= 0:
        ifint = True
    else:
        ifint = False
    # 整数部分
    for i in reversed(bb):
        count = count + 1
        if (int(i) == 0):
            if (flag == True):
                if (count != 5):
                    continue
                else:
                    money = dict2[count] + money
            else:
                if (flag2 == False):
                    money = dict2[count] + money
                else:
                    if (count != 5):
                        money = '零' + money
                    else:
                        money = dict2[count] + '零' + money
            flag = True
        else:
            flag = False
            flag2 = True
            money = dict1[int(i)] + dict2[count] + money
    # 小数部分
    for i in cc:
        count2 = count2 + 1
        money = money + dict1[int(i)] + dict2[count2]
    if (ifint == True):
        money = money + '整'
    return money


if __name__ == '__main__':
    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING)
    dl = DataLoader()
    dl.load()
    c = Contract(dl,'中山市湘华电力科技有限公司', '广州')
    c.add_item(1, 20, 0.8)
    c.add_item(0, 10, 0.9)
    c.display_table()
    print()
    c.del_item(0)
    c.display_table()
    c.add_item(0,10,0.9)
    print(c.get_total_daxie())
