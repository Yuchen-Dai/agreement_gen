from dataLoader import DataLoader
from contract import Contract
from pathlib import Path
from product import Product
from exception import FileOccupied

import xlsxwriter, os, logging


class Excel:
    def __init__(self, contract):
        self.c = contract

    def run(self, file_dir='Output/Expenses', output_type=None):  # todo 类型2报价单需要添加
        border = 1
        if not file_dir.endswith('.xlsx'):
            p = Path(file_dir + ".xlsx")
        else:
            p = Path(file_dir)
        workbook = xlsxwriter.Workbook(p)

        right_bottom = workbook.add_format({'right': border, 'bottom': border, 'align': 'left', 'valign': 'vcenter'})
        left_bottom = workbook.add_format({'left': border, 'bottom': border, 'align': 'left', 'valign': 'vcenter'})
        left = workbook.add_format({'left': border, 'align': 'left', 'valign': 'vcenter'})
        right = workbook.add_format({'right': border, 'align': 'left', 'valign': 'vcenter'})
        vcenter = workbook.add_format({'valign': 'vcenter'})

        merge_format0 = workbook.add_format({
            'bold': True,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',  # 字体
            'font_size': 22,
        })

        merge_format1 = workbook.add_format({
            'bold': True,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',  # 字体
            'font_size': 14,
        })

        merge_format2 = workbook.add_format({
            'align': 'right',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',  # 字体
            'font_size': 11,
        })

        merge_format3 = workbook.add_format({
            'border': border,
            'bold': True,
            'align': 'left',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',  # 字体
            'font_size': 11,
        })

        merge_format4_bold = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font': '宋体',  # 字体
            'font_size': 11,
        })

        merge_format4 = workbook.add_format({
            'font': '宋体',
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 11,
        })

        merge_format5 = workbook.add_format({
            'align': 'left',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',  # 字体
            'font_size': 11,
        })

        format1 = workbook.add_format({
            'border': border,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',
            'font_size': 11,
        })
        format1.set_text_wrap()

        format1_left_top = workbook.add_format({
            'left': border,
            'top': border,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',
            'font_size': 11,
        })

        format1_right_top = workbook.add_format({
            'right': border,
            'top': border,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',
            'font_size': 11,
        })

        format1_bold = workbook.add_format({
            'border': border,
            'bold': True,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',
            'font_size': 11,
        })

        number_format1 = workbook.add_format({
            'border': border,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',
            'font_size': 11,
            'num_format': '0.00',
        })

        number_format2_bold = workbook.add_format({
            'border': border,
            'bold': True,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'font': '宋体',
            'font_size': 11,
            'num_format': '0.00',
        })

        if output_type == 1:
            # 销售合同
            # sheet1
            sheet1 = workbook.add_worksheet('销售合同')
            sheet1.set_margins()
            sheet1.set_row(0, 30)
            sheet1.set_column(0, 0, 4)
            sheet1.set_column(1, 1, 15)
            sheet1.set_column(2, 2, 25)
            sheet1.set_column(3, 5, 5)
            sheet1.set_column(6, 6, 10)
            sheet1.set_column(7, 7, 14)

            sheet1.merge_range(0, 0, 0, 7, '购销合同', merge_format0)
            write_nonbold_bold(sheet1, 2, 0, 2, 5, merge_format4, merge_format4_bold, '供方：', self.c.get_supplier())
            write_nonbold_bold(sheet1, 3, 0, 3, 5, merge_format4, merge_format4_bold, '需方：', self.c.get_buyer())
            write_nonbold_bold(sheet1, 2, 6, 2, 7, merge_format4, merge_format4_bold, '合同编号：',
                               self.c.get_contract_num())
            write_nonbold_bold(sheet1, 3, 6, 3, 7, merge_format4, merge_format4_bold, '签订地点：', self.c.get_location())
            write_nonbold_bold(sheet1, 4, 6, 4, 7, merge_format4, merge_format4_bold, '签订时间：', self.c.get_sign_date())
            sheet1.merge_range(4, 0, 4, 5, '一、产品名称、商标、型号、厂家、数量、金额、供货时间', merge_format5)

            for col in range(8):
                sheet1.write(5, col, ['序号', '品牌', '规格型号', '单位', '数量', '单价', '结算金额', '备注'][col], format1_bold)
            row = 6
            for i, (brand, price) in enumerate(self.c.get_brand(), 1):
                sheet1.write(row, 0, i, format1)
                sheet1.write(row, 1, brand, format1)
                sheet1.merge_range(row, 2, row, 5, '详见合同第二页', format1_bold)
                sheet1.write(row, 6, price, number_format1)
                sheet1.write(row, 7, None, format1_bold)
                row += 1

            sheet1.merge_range(row, 0, row, 5, f'合计人民币金额（大写）：{self.c.get_total_daxie()}', merge_format3)
            sheet1.write(row, 6, self.c.get_total(), number_format2_bold)
            sheet1.write(row, 7, '含13%增值税', format1_bold)
            write_nonbold_bold(sheet1, row + 1, 0, row + 1, 7, merge_format4, merge_format4_bold,
                               '二、质量要求技术标准：', self.c.get_zhiliang(), vcenter)
            write_nonbold_bold(sheet1, row + 2, 0, row + 2, 7, merge_format4, merge_format4_bold,
                               '三、交（提）货时间及地点方式：', self.c.get_jiaohuo(), vcenter)
            write_nonbold_bold(sheet1, row + 3, 0, row + 3, 7, merge_format4, merge_format4_bold,
                               '四、运输方式及到达站点和费用负担：', self.c.get_yunshu(), vcenter)
            write_nonbold_bold(sheet1, row + 4, 0, row + 4, 7, merge_format4, merge_format4_bold,
                               '五、合理损耗及计算方法：', self.c.get_heli(), vcenter)
            write_nonbold_bold(sheet1, row + 5, 0, row + 5, 7, merge_format4, merge_format4_bold,
                               '六、包装标准，包装物的供应及回收：', self.c.get_baozhuang(), vcenter)
            write_nonbold_bold(sheet1, row + 6, 0, row + 6, 7, merge_format4, merge_format4_bold,
                               '七、验收标准及提出异议时间：', self.c.get_yanshou(), vcenter)
            sheet1.merge_range(row + 7, 0, row + 7, 7, '八、标的物所有权自供方收到货款之日起转移给需方，在需方未履行（支付款项/100%货款）'
                                                       '义务前，', merge_format4)
            sheet1.merge_range(row + 8, 0, row + 8, 7, '    标的物仍属于供方所有，标的物毁损，灭失等风险自交付时起由需方承担。',
                               merge_format4)
            write_nonbold_bold(sheet1, row + 9, 0, row + 9, 7, merge_format4, merge_format4_bold,
                               '九、结算方式及期限：', self.c.get_jiesuan(), vcenter)
            write_nonbold_bold(sheet1, row + 10, 0, row + 10, 7, merge_format4, merge_format4_bold,
                               '十、如需提供担保，另立合同担保书，作为本合同附件：', self.c.get_ruxu(), vcenter)
            write_nonbold_bold(sheet1, row + 11, 0, row + 11, 7, merge_format4, merge_format4_bold,
                               '十一、违约责任：', self.c.get_weiyue(), vcenter)
            write_nonbold_bold(sheet1, row + 12, 0, row + 12, 7, merge_format4, merge_format4_bold,
                               '十二、解决合同纠纷的方式：', self.c.get_jiejue(), vcenter)
            row += 13
            flag = True
            for i in self.c.get_qita():
                if flag:
                    write_nonbold_bold(sheet1, row, 0, row, 7, merge_format4, merge_format4_bold,
                                       '十三、其它约定事情:', i, vcenter)
                    flag = False
                else:
                    sheet1.merge_range(row, 0, row, 7, f'                {i}', merge_format4_bold)
                row += 1

            row += 1
            supplier_info = self.c.get_supplier_info()
            buyer_info = self.c.get_buyer_info()
            sheet1.merge_range(row, 0, row, 2, '供方', format1_left_top)
            sheet1.merge_range(row, 3, row, 7, '需方', format1_right_top)
            write_nonbold_bold(sheet1, row + 1, 0, row + 1, 2, merge_format4, merge_format4,
                               '单位名称（章）：', supplier_info[0], left)
            write_nonbold_bold(sheet1, row + 1, 3, row + 1, 7, merge_format4, merge_format4,
                               '单位名称（章）：', buyer_info[0], right)
            write_nonbold_bold(sheet1, row + 2, 0, row + 2, 2, merge_format4, merge_format4,
                               '单位地址：', supplier_info[1], left)
            write_nonbold_bold(sheet1, row + 2, 3, row + 2, 7, merge_format4, merge_format4,
                               '单位地址：', buyer_info[1], right)
            sheet1.merge_range(row + 3, 0, row + 3, 2, '法定代表人：', left)
            sheet1.merge_range(row + 3, 3, row + 3, 7, '法定代表人：', right)
            sheet1.merge_range(row + 4, 0, row + 4, 2, '委托代表人：', left)
            sheet1.merge_range(row + 4, 3, row + 4, 7, '委托代表人：', right)
            sheet1.merge_range(row + 5, 0, row + 5, 2, '签字日期：', left)
            sheet1.merge_range(row + 5, 3, row + 5, 7, '签字日期：', right)
            write_nonbold_bold(sheet1, row + 6, 0, row + 6, 2, merge_format4, merge_format4,
                               '开户银行', supplier_info[2], left)
            write_nonbold_bold(sheet1, row + 6, 3, row + 6, 7, merge_format4, merge_format4,
                               '开户银行：', buyer_info[2], right)
            write_nonbold_bold(sheet1, row + 7, 0, row + 7, 2, merge_format4, merge_format4,
                               '帐号：', supplier_info[3], left)
            write_nonbold_bold(sheet1, row + 7, 3, row + 7, 7, merge_format4, merge_format4,
                               '帐号：', buyer_info[3], right)
            write_nonbold_bold(sheet1, row + 8, 0, row + 8, 2, merge_format4, merge_format4,
                               '税证号码：', supplier_info[4], left)
            write_nonbold_bold(sheet1, row + 8, 3, row + 8, 7, merge_format4, merge_format4,
                               '税证号码：', buyer_info[4], right)
            write_nonbold_bold(sheet1, row + 9, 0, row + 9, 2, merge_format4, merge_format4,
                               '电话：', supplier_info[5], left_bottom)
            write_nonbold_bold(sheet1, row + 9, 3, row + 9, 7, merge_format4,
                               merge_format4, '电话：', buyer_info[5], right_bottom)
            sheet1.insert_image(row + 1, 0, 'img\\stamp1.png', {'x_offset': 40})

            for i in range(1, row + 11):
                sheet1.set_row(i, 20)

            # sheet2
            sheet2 = workbook.add_worksheet('合同清单')
            sheet2.set_margins()
            sheet2.set_row(0, 30)
            sheet2.set_column(0, 0, 4)
            sheet2.set_column(1, 1, 15)
            sheet2.set_column(2, 2, 22)
            sheet2.set_column(3, 4, 4)
            sheet2.set_column(5, 7, 0)
            sheet2.set_column(8, 9, 10)
            sheet2.set_column(10, 10, 14)

            sheet2.merge_range(0, 0, 0, 10, '购销合同清单', merge_format1)
            sheet2.merge_range(1, 0, 1, 10, f'合同编号：{self.c.get_contract_num()}', merge_format2)

            for col in range(11):
                sheet2.write(2, col, ['序号', '产品名称', '型号及规格', '单位', '数量', '面价', '折扣',
                                      '附件', '单价', '金额', '备注'][col], format1_bold)
            row, col = 3, 0
            for product, number, discount, comment in self.c.get_table():
                sheet2.write(row, col, row - 2, format1)  # 序号
                sheet2.write(row, col + 1, product.get_name(), format1)  # 产品名称
                sheet2.write(row, col + 2, product.get_specs(), format1)  # 型号及规格
                sheet2.write(row, col + 3, product.get_unit(), format1)  # 单位
                sheet2.write(row, col + 4, number, format1)  # 数量
                sheet2.write_number(row, col + 5, product.get_raw_price(), number_format1)  # 面价
                sheet2.write(row, col + 6, discount, format1)  # 折扣
                sheet2.write_number(row, col + 7, product.get_adjunct_price(), number_format1)  # 附件
                sheet2.write_formula(row, col + 8, f'=F{row + 1}*G{row + 1}+H{row + 1}', number_format1)  # 单价
                sheet2.write_formula(row, col + 9, f'=E{row + 1}*I{row + 1}', number_format1)  # 金额
                sheet2.write(row, col + 10, None, format1)  # 备注
                row += 1
            for i in range(11):
                sheet2.write(row, i, None, format1_bold)
            sheet2.write(row, col + 1, '合计', format1_bold)
            sheet2.write_formula(row, col + 4, f'=SUM(E4:E{row})', format1_bold)
            sheet2.write_formula(row, col + 9, f'=SUM(J4:J{row})', number_format2_bold)
            sheet2.merge_range(row + 1, 0, row + 1, 10, f'合计人民币金额（大写）：{self.c.get_total_daxie()}', merge_format3)
            write_nonbold_bold(sheet2, row + 3, 0, row + 3, 2, merge_format4, merge_format4_bold, '单位名称（章）：',
                               self.c.get_supplier(), vcenter)
            write_nonbold_bold(sheet2, row + 3, 3, row + 3, 10, merge_format4, merge_format4_bold, '单位名称（章）：',
                               self.c.get_buyer(), vcenter)
            sheet2.merge_range(row + 5, 0, row + 5, 2, '日期：', merge_format4)
            sheet2.merge_range(row + 5, 3, row + 5, 10, '日期：', merge_format4)
            sheet2.insert_image(row, 1, 'img\\stamp1.png')

        elif output_type == 2:
            # 报价单
            row = 0
            sheet1 = workbook.add_worksheet('报价单')
            sheet1.set_margins()
            sheet1.set_row(0, 30)
            sheet1.set_column(0, 0, 4)
            sheet1.set_column(1, 1, 15)
            sheet1.set_column(2, 2, 22)
            sheet1.set_column(3, 4, 4)
            sheet1.set_column(5, 7, 0)
            sheet1.set_column(8, 9, 10)
            sheet1.set_column(10, 10, 14)

            sheet1.merge_range(0, 0, 0, 10, '广州市森源电气有限公司报价单', merge_format1)
            write_nonbold_bold(sheet1, 2, 0, 2, 2, merge_format4, merge_format4_bold, '客户名称：', self.c.get_buyer_name())
            write_nonbold_bold(sheet1, 2, 3, 2, 10, merge_format4, merge_format4_bold, '报价单号：', self.c.get_qid())
            write_nonbold_bold(sheet1, 3, 0, 3, 2, merge_format4, merge_format4_bold, '项目名称：',
                               self.c.get_project_name())
            write_nonbold_bold(sheet1, 3, 3, 3, 10, merge_format4, merge_format4_bold, '报价联系人：',
                               self.c.get_quote_contact())
            write_nonbold_bold(sheet1, 4, 0, 4, 2, merge_format4, merge_format4_bold, '客户联系人：',
                               self.c.get_buyer_contact())
            write_nonbold_bold(sheet1, 4, 3, 4, 10, merge_format4, merge_format4_bold, '电话/传真：', self.c.get_quote_tel())
            write_nonbold_bold(sheet1, 5, 0, 5, 2, merge_format4, merge_format4_bold, '客户电话/传真：',
                               self.c.get_buyer_tel())
            write_nonbold_bold(sheet1, 5, 3, 5, 10, merge_format4, merge_format4_bold, 'QQ：', self.c.get_qq())
            sheet1.merge_range(6, 0, 6, 10, '贵司垂询的产品报价如下：', merge_format4)

            for col in range(11):
                sheet1.write(7, col, ['序号', '产品名称', '型号及规格', '单位', '数量', '面价', '折扣',
                                      '附件', '单价', '金额', '备注'][col], format1_bold)
            row = 8
            col = 0
            for product, number, discount, comment in self.c.get_table():
                sheet1.write(row, col, row - 7, format1)  # 序号
                sheet1.write(row, col + 1, product.get_name(), format1)  # 产品名称
                sheet1.write(row, col + 2, product.get_specs(), format1)  # 型号及规格
                sheet1.write(row, col + 3, product.get_unit(), format1)  # 单位
                sheet1.write(row, col + 4, number, format1)  # 数量
                sheet1.write_number(row, col + 5, product.get_raw_price(), number_format1)  # 面价
                sheet1.write(row, col + 6, discount, format1)  # 折扣
                sheet1.write_number(row, col + 7, product.get_adjunct_price(), number_format1)  # 附件
                sheet1.write_formula(row, col + 8, f'=F{row + 1}*G{row + 1}+H{row + 1}', number_format1)  # 单价
                sheet1.write_formula(row, col + 9, f'=E{row + 1}*I{row + 1}', number_format1)  # 金额
                sheet1.write(row, col + 10, comment, format1)  # 备注
                row += 1
            for i in range(11):
                sheet1.write(row, i, None, format1_bold)
            sheet1.write(row, col + 1, '合计', format1_bold)
            sheet1.write_formula(row, col + 4, f'=SUM(E4:E{row})', format1_bold)
            sheet1.write_formula(row, col + 9, f'=SUM(J4:J{row})', number_format2_bold)
            row += 1
            write_nonbold_bold(sheet1, row, 0, row, 10, merge_format4, merge_format4_bold, '备注:', self.c.get_comment())
            write_nonbold_bold(sheet1, row+1, 0, row+1, 10, merge_format4, merge_format4_bold, '日期:', '.'.join(self.c.get_date()))
            write_nonbold_bold(sheet1, row+2, 0, row+2, 10, merge_format4, merge_format4_bold, '报价人:', self.c.get_quote_contact())

        workbook.close()


def write_nonbold_bold(sheet, frow, fcol, lrow, lcol, format_nonbold, format_bold, s1, s2, merge_format=None):
    if not merge_format:
        sheet.merge_range(frow, fcol, lrow, lcol, None, format_nonbold)
        sheet.write_rich_string(frow, fcol, format_nonbold, s1, format_bold, s2)
    else:
        sheet.merge_range(frow, fcol, lrow, lcol, None, merge_format)
        sheet.write_rich_string(frow, fcol, format_nonbold, s1, format_bold, s2, merge_format)


if __name__ == '__main__':
    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING)
    dl = DataLoader()

    a = Product('塑壳断路器', 'RMM1-630S/3310', '500A', '台', 1220.00, [("抽屉式", 180), ("VC3", 30.1)])
    b = Product('交流塑壳断路', 'RMM1-100S/3300', '160A', '只', 174, [("带电剩余保护模块", 88)])
    c = Product('微型断路器', 'RMC3-63', "", "只", 94.2, [("带剩余电流保护模块AC型 30mA", 16)])
    dl.add_data(a)
    dl.add_data(b)
    dl.add_data(c)

    c = Contract(supplier='广州市森源电气有限公司', buyer='中山市湘华电力科技有限公司', brand='广州人民',
                 sign_date=('2021', '7', '23'), location='广州',
                 contract_number='00000009')
    c.others = ['123333', '22333333']
    c.add_item(dl[1], 20, 0.8, '')
    c.add_item(dl[0], 10, 0.9, '')

    test = Excel(c)
    test.run()
