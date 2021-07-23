import logging
import os
import time
import exception
import pickle
from pathlib import Path
from dataLoader import DataLoader
from product import Product

class Contract:
    def __init__(self, supplier, buyer, brand, sign_date, delivery_date, location, payment_method, comments, others:[],
                 supplier_location, supplier_bank, supplier_account, supplier_tax_num, supplier_tel,
                 buyer_location,    buyer_bank,    buyer_account,    buyer_tax_num,    buyer_tel):
        self.location = location
        self.supplier = supplier
        self.brand = brand
        self.buyer = buyer
        self.sign_date = sign_date
        self.delivery_date = delivery_date
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

        self.table = []  # [(product_id, quantity, discount)]

    def add_item(self, product, quantity, discount=1):
        assert type(product) == Product
        self.table.append((product, quantity, discount))

    def del_item(self, line_number):
        logging.info(f"Del line: {line_number}")
        del self.table[line_number]

    def get_sign_date(self):
        if not self.sign_date:
            return time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')  # 例：2021年7月23日
        else:
            return self.sign_date

    def display_table(self):
        for i, line in enumerate(self.table):
            print(i, line[0], 'quantity:', line[1], 'discount:', line[2])

    def get_contract_num(self):
        pass  # todo 自动获取，并且可更改
        return '21051425'

    def get_location(self):
        """签订地点"""
        return self.location

    def get_supplier_info(self) -> 'company_name, company_location, company_bank, account#, tax#, tel#':
        return self.get_supplier(), self.supplier_location, self.supplier_bank, \
               self.supplier_account, self.supplier_tax_num, self.supplier_tel

    def get_buyer_info(self) -> 'company_name, company_location, company_bank, account#, tax#, tel#':
        return self.get_buyer(), self.buyer_location, self.buyer_bank, \
               self.buyer_account, self.buyer_tax_num, self.buyer_tel

    def get_buyer(self):
        return self.buyer

    def get_supplier(self):
        return self.supplier

    def get_total(self):
        total = 0
        for line in self.table:
            p = line[0]
            total += line[1] * (p.get_raw_price() * line[2] + p.get_adjunct_price())
        return total

    def get_total_daxie(self):
        return numToBig(self.get_total())

    def get_brand(self):
        yield self.brand, self.get_total()

    def get_table(self):
        return self.table

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
        return self.payment_method

    def get_ruxu(self):  # 十、如需提供担保，另立合同担保书，作为本合同附件
        return f'空白。'

    def get_weiyue(self):  # 十一、违约责任
        return f'按《合同法》执行。 '

    def get_jiejue(self):  # 十二、解决合同纠纷的方式
        return f'双方协商解决，协商不成可向供方所在地人民法院提起诉讼。'

    def get_qita(self):  # 十三、其它约定事情
        return self.others

    def save(self, dir = 'data/contract'):
        assert self.get_contract_num(), "Need to have a contract number to save"
        cnum = self.get_contract_num()
        p = Path(dir) / cnum[:2] / cnum[2:4]
        if not p.exists():
            logging.info(f"Create saving directory: {p.resolve}")
            p.mkdir(parents=True)
        p = p / f'{cnum}.data'
        logging.info(f"Save data: {p.resolve()}")
        with p.open('wb') as f:
            pickle.dump(self.__dict__, f)

    @staticmethod
    def load(cnum, dir = 'data/contract'):
        cnum = str(cnum)
        assert len(cnum) == 8, f'Not a valid contract number{cnum}'
        p = Path(dir) / cnum[:2] / cnum[2:4] / f'{str(cnum)}.data'
        assert p.exists(), f"No existing file: {p}"
        c = Contract(None,None,None)
        with p.open('rb') as pkl_file:
            c.__dict__ = pickle.load(pkl_file)
        logging.info(f"Load data from file: {p.resolve()}")
        return c

    @staticmethod
    def delete(cnum, dir = 'data/contract'):
        cnum = str(cnum)
        assert len(cnum) == 8, f'Not a valid contract number{cnum}'
        p = Path(dir) / cnum[:2] / cnum[2:4] / f'{str(cnum)}.data'
        assert p.exists(), f"No existing file: {p}"
        logging.info(f"Delete contract: {p.resolve()}")
        p.unlink()

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
    dl = DataLoader.load()

    try:
        dl.add_data('塑壳断路器', '台', 1220, 130, model='RMM1-630S/3310', current='500A')
        dl.add_data('塑壳断路器', '台', 1220, 130, model='RMM1-400S/3310', current='350A')
        dl.save()
    except exception.productAlreadyExist:
        pass
    c = Contract.load('21051425')
    # c.add_item(dl[0], 20, 0.8)
    # c.add_item(dl[1], 10, 0.9)
    # c.display_table()
    # print()
    # c.del_item(1)
    # c.display_table()
    # c.add_item(dl[1], 10, 0.9)
    # print(c.get_total_daxie())
    c.display_table()
