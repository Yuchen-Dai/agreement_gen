import logging
import os
import datetime
import pickle
from pathlib import Path
from exception import ContractNumberAlreadyExist, IllegalDate, FileExceed


class Contract:
    def __init__(self, supplier='', buyer='', brand='', sign_date=('1970', '01', '01',), delivery_date='',
                 delivery_location='',
                 location='', payment_method='', comments='', others=[], supplier_location='',
                 supplier_bank='', supplier_account='', supplier_tax_num='', supplier_tel='',
                 buyer_location='', buyer_bank='', buyer_account='', buyer_tax_num='', buyer_tel='',
                 name='', contract_number=''):
        self.location = location
        self.supplier = supplier
        self.brand = brand
        self.buyer = buyer
        assert type(sign_date) == tuple
        assert len(sign_date) == 3
        assert all([type(i) == str for i in sign_date])
        try:
            self.sign_date = datetime.datetime(int(sign_date[0]), int(sign_date[1]), int(sign_date[2]))
        except ValueError:
            raise IllegalDate
        self.delivery_date = delivery_date
        self.delivery_location = delivery_location
        self.payment_method = payment_method
        self.comments = comments
        assert type(others) == list
        self.others = others
        self.supplier_location = supplier_location
        self.supplier_bank = supplier_bank
        self.supplier_account = supplier_account
        self.supplier_tax_num = supplier_tax_num
        self.supplier_tel = supplier_tel
        self.buyer_location = buyer_location
        self.buyer_bank = buyer_bank
        self.buyer_account = buyer_account
        self.buyer_tax_num = buyer_tax_num
        self.buyer_tel = buyer_tel
        self.name = name
        self.cid = contract_number
        self._is_template = True
        self._new = True
        self._modify = True

        self.table = []  # [(product_id, quantity, discount)]

    def get_table(self):
        return self.table

    def update_sign_date(self, sign_date):
        assert type(sign_date) == tuple
        assert len(sign_date) == 3
        assert all([type(i) == str for i in sign_date])
        try:
            self.sign_date = datetime.datetime(int(sign_date[0]), int(sign_date[1]), int(sign_date[2]))
        except ValueError:
            raise IllegalDate

    def get_name(self):
        return self.name if self.name else self.get_contract_num()

    def add_item(self, product, quantity, discount, comments):
        logging.info(f"Add line: {product}")
        self.table.append((product, quantity, discount, comments))
        self.table.sort(key=lambda x: x[0])
        self._modify = True

    def del_item(self, line_number):
        logging.info(f"Del line: {line_number}")
        del self.table[line_number]
        self._modify = True

    def get_sign_date(self):
        if not self.sign_date:
            today = datetime.date.today()
            return '{}年{:0>2d}月{:0>2d}日'.format(today.year, today.month, today.day)  # 例：2021年7月23日
        else:
            return '{}年{:0>2d}月{:0>2d}日'.format(self.sign_date.year, self.sign_date.month, self.sign_date.day)

    def display_table(self):
        for i, line in enumerate(self.table):
            print(i, line[0], 'quantity:', line[1], 'discount:', line[2])

    def get_contract_num(self):
        return self.cid if self.cid else ' '

    def get_location(self):
        """签订地点"""
        return self.location if self.location else ' '

    def get_supplier_info(self) -> 'company_name, company_location, company_bank, account#, tax#, tel#':
        return self.get_supplier(), self.supplier_location if self.supplier_location else ' ', \
               self.supplier_bank if self.supplier_bank else ' ', \
               self.supplier_account if self.supplier_account else ' ', self.supplier_tax_num if self.supplier_tax_num \
                   else ' ', self.supplier_tel if self.supplier_tel else ' '

    def get_buyer_info(self) -> 'company_name, company_location, company_bank, account#, tax#, tel#':
        return self.get_buyer(), self.buyer_location if self.buyer_location else ' ', self.buyer_bank if self.buyer_bank else ' ', \
               self.buyer_account if self.buyer_account else ' ', self.buyer_tax_num if self.buyer_tax_num else ' ', \
               self.buyer_tel if self.buyer_tel else ' '

    def get_buyer(self):
        return self.buyer if self.buyer else ' '

    def get_supplier(self):
        return self.supplier if self.supplier else ' '

    def get_total_quantity(self):
        total = 0
        for line in self.table:
            total += line[1]
        return total

    def get_total(self):
        total = 0
        for line in self.table:
            p = line[0]
            total += line[1] * (p.get_raw_price() * line[2] + p.get_adjunct_price())
        return total

    def get_total_daxie(self):
        return numToBig(self.get_total())

    def get_brand(self):
        return [(self.brand if self.brand else ' ', self.get_total())]

    def get_zhiliang(self):  # 二、质量要求技术标准
        return '按国家有关质量标准及需方技术要求。 '

    def get_jiaohuo(self):  # 三、交（提）货时间及地点方式
        return f'合同生效后{self.delivery_date}个工作日货到{self.location}。'

    def get_yunshu(self):  # 四、运输方式及到达站点和费用负担
        return f'汽运，汽运费供方承担。'

    def get_heli(self):  # 五、合理损耗及计算方法
        return f'空白。'

    def get_baozhuang(self):  # 六、包装标准，包装物的供应及回收：
        return f'纸箱包装，包装物不回收。'

    def get_yanshou(self):  # 七、验收标准及提出异议时间：
        return f'按国家有关标准验收.如有质量问题，货到7天内书面通知供方。'

    def get_biaode(self):
        # '八、标的物所有权自供方收到货款之日起转移给需方，在需方未履行（支付款项/100%货款）义务前，
        # 标的物仍属于供方所有，标的物毁损，灭失等风险自交付时起由需方承担。'
        return f'空白。'

    def get_jiesuan(self):  # 九、结算方式及期限
        return self.payment_method if self.payment_method else '空白。'

    def get_ruxu(self):  # 十、如需提供担保，另立合同担保书，作为本合同附件
        return f'空白。'

    def get_weiyue(self):  # 十一、违约责任
        return f'按《合同法》执行。 '

    def get_jiejue(self):  # 十二、解决合同纠纷的方式
        return f'双方协商解决，协商不成可向供方所在地人民法院提起诉讼。'

    def get_qita(self):  # 十三、其它约定事情
        return self.others

    def set_template(self, set_t: bool):
        self._is_template = set_t

    def save(self, dir='data/contract'):
        p = Path(dir)
        if self._is_template:
            p = p / 'template'
            if not self.cid:
                if not p.exists():
                    self.cid = '00000001'
                else:
                    check_occupy = [True] * 99
                    for i in p.iterdir():
                        if i.stem.startswith('0000'):
                            check_occupy[int(i.stem[6:8]) - 1] = False
                    last_two = None
                    for i, not_occupy in enumerate(check_occupy):
                        if not_occupy:
                            last_two = i + 1
                            break
                    if not last_two:
                        raise FileExceed(f'Contract for template exceed 100.')
                    self.cid = '000000{:0>2d}'.format(last_two)

        else:
            p = p / 'contract'

        if not p.exists():
            logging.info(f"Create saving directory: {p.resolve()}")
            p.mkdir(parents=True)
        p = p / f'{self.cid}.data'
        if p.exists() and self._new:
            raise ContractNumberAlreadyExist
        self._new = False
        if self._modify:
            self._modify = False
            logging.info(f"Save data: {p.resolve()}")
            with p.open('wb') as f:
                pickle.dump(self.__dict__, f)
        else:
            logging.info(f"No modify, did not save: {p.resolve()}")

    def delete(self, dir='data/contract'):
        cid = self.cid
        p = Path(dir)
        if cid.startswith('0000'):
            p = p / 'template'
        else:
            p = p / 'contract'
        p = p / f'{str(cid)}.data'
        assert p.exists(), f"No existing file: {p}"
        logging.info(f"Delete contract: {p.resolve()}")
        p.unlink()

    @staticmethod
    def load(cid, dir='data/contract'):
        c = Contract()
        if cid.startswith('0000'):
            p = Path(dir) / 'template' / f'{str(cid)}.data'
            assert p.exists(), f"No existing file: {p}"
            with p.open('rb') as pkl_file:
                c.__dict__ = pickle.load(pkl_file)
            logging.info(f"Load template from file: {p.resolve()}")
        else:
            p = Path(dir) / 'contract' / f'{str(cid)}.data'
            assert p.exists(), f"No existing file: {p}"
            with p.open('rb') as pkl_file:
                c.__dict__ = pickle.load(pkl_file)
            logging.info(f"Load contract from file: {p.resolve()}")
        c._modify = False
        return c

    @staticmethod
    def copy(other):
        c = Contract()
        if type(other) == Contract:
            c.location = other.location
            c.supplier = other.supplier
            c.brand = other.brand
            c.buyer = other.buyer
            c.sign_date = datetime.datetime(other.sign_date.year, other.sign_date.month, other.sign_date.day)
            c.delivery_date = other.delivery_date
            c.delivery_location = other.delivery_location
            c.payment_method = other.payment_method
            c.comments = other.comments
            c.others = [i for i in other.others]
            c.supplier_location = other.supplier_location
            c.supplier_bank = other.supplier_bank
            c.supplier_account = other.supplier_account
            c.supplier_tax_num = other.supplier_tax_num
            c.supplier_tel = other.supplier_tel
            c.buyer_location = other.buyer_location
            c.buyer_bank = other.buyer_bank
            c.buyer_account = other.buyer_account
            c.buyer_tax_num = other.buyer_tax_num
            c.buyer_tel = other.buyer_tel
            c.name = other.name
        return c


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
    from dataLoader import DataLoader
    from product import Product

    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    # dl = DataLoader()
    #
    # a = Product('塑壳断路器', 'RMM1-630S/3310', '500A', '台', 1220.00, [("抽屉式", 180), ("VC3", 30.1)])
    # b = Product('交流塑壳断路', 'RMM1-100S/3300', '160A', '只', 174, [("带电剩余保护模块", 88)])
    # c = Product('微型断路器', 'RMC3-63', "", "只", 94.2, [("带剩余电流保护模块AC型 30mA", 16)])
    # dl.add_data(a)
    # dl.add_data(b)
    # dl.add_data(c)
    #
    # c = Contract(supplier='广州市森源电气有限公司', buyer='中山市湘华电力科技有限公司', brand='广州人民',
    #              sign_date=('2021', '5', '7'), location='广州')
    # c.add_item(dl[1], 20, 0.8)
    # c.add_item(dl[0], 10, 0.9)

    # c.display_table()
    # print(list(Contract.get_contract_list()))
    c = Contract.load('00000001')
    c.save()
