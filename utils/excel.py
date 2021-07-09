import logging
from dataLoader import DataLoader
from contract import Contract

import xlsxwriter, os, logging
from pathlib import Path


class Excel:
    def __init__(self, Contract, dl):
        self.c = Contract
        self.dl = dl

    def run(self, filename='Expenses.xlsx', dir='output'):
        border = 1
        p = Path(dir)
        if not p.exists():
            logging.info(f'No existing output directory, create: {p.resolve()}')
            p.mkdir(parents=True)
        workbook = xlsxwriter.Workbook(p / filename)

        right_bottom = workbook.add_format({'right': border, 'bottom': border,'align': 'left',  'valign': 'vcenter'})
        left_bottom = workbook.add_format({'left': border, 'bottom': border,'align': 'left',  'valign': 'vcenter'})
        left = workbook.add_format({'left': border, 'align': 'left',  'valign': 'vcenter'})
        right = workbook.add_format({'right': border, 'align': 'left',  'valign': 'vcenter'})

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
            'font': '宋体',  # 字体
            'font_size': 11,
        })
        merge_format4_bold.set_text_wrap()

        merge_format4 = workbook.add_format({
            'font': '宋体',  # 字体
            'font_size': 11,
        })
        merge_format4.set_text_wrap()

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

        # sheet1
        sheet1 = workbook.add_worksheet('销售合同')
        sheet1.set_row(0, 30)
        sheet1.set_column(0, 0, 5)
        sheet1.set_column(1, 1, 25)
        sheet1.set_column(2, 2, 30)
        sheet1.set_column(3, 5, 10)
        sheet1.set_column(6, 6, 15)
        sheet1.set_column(7, 7, 27)

        sheet1.merge_range('A1:H1', '购销合同', merge_format0)
        write_nonbold_bold(sheet1, 'A3:F3', merge_format4, merge_format4_bold, '供方：', c.get_supplier())
        write_nonbold_bold(sheet1, 'A4:F4', merge_format4, merge_format4_bold, '需方：', c.get_buyer())
        write_nonbold_bold(sheet1, 'G3:H3', merge_format4, merge_format4_bold, '合同编号：', c.get_contract_num())
        write_nonbold_bold(sheet1, 'G4:H4', merge_format4, merge_format4_bold, '签订地点：', c.get_location())
        write_nonbold_bold(sheet1, 'G5:H5', merge_format4, merge_format4_bold, '签订时间：', c.get_date())
        sheet1.merge_range('A5:F5', '一、产品名称、商标、型号、厂家、数量、金额、供货时间', merge_format5)

        for col in range(8):
            sheet1.write(5, col, ['序号', '品牌', '规格型号', '单位', '数量', '单价', '结算金额', '备注'][col], format1_bold)
        row = 6
        for i, (brand, price) in enumerate(self.c.get_brand(), 1):
            sheet1.write(row, 0, i, format1)
            sheet1.write(row, 1, brand, format1)
            sheet1.merge_range(f'C{row + 1}:F{row + 1}', '详见合同第二页', format1_bold)
            sheet1.write(row, 6, price, number_format1)
            sheet1.write(row, 7, None, format1_bold)
            row += 1
        sheet1.merge_range(f'A{row + 1}:F{row + 1}', f'合计人民币金额（大写）：{self.c.get_total_daxie()}', merge_format3)
        sheet1.write(row, 6, self.c.get_total(), number_format2_bold)
        sheet1.write(row, 7, '含13%增值税', format1_bold)
        write_nonbold_bold(sheet1, f'A{row + 2}:H{row + 2}', merge_format4, merge_format4_bold,
                           '二、质量要求技术标准：', self.c.get_zhiliang())
        write_nonbold_bold(sheet1, f'A{row + 3}:H{row + 3}', merge_format4, merge_format4_bold,
                           '三、交（提）货时间及地点方式：', self.c.get_jiaohuo())
        write_nonbold_bold(sheet1, f'A{row + 4}:H{row + 4}', merge_format4, merge_format4_bold,
                           '四、运输方式及到达站点和费用负担：', self.c.get_yunshu())
        write_nonbold_bold(sheet1, f'A{row + 5}:H{row + 5}', merge_format4, merge_format4_bold,
                           '五、合理损耗及计算方法：', self.c.get_heli())
        write_nonbold_bold(sheet1, f'A{row + 6}:H{row + 6}', merge_format4, merge_format4_bold,
                           '六、包装标准，包装物的供应及回收：', self.c.get_baozhuang())
        write_nonbold_bold(sheet1, f'A{row + 7}:H{row + 7}', merge_format4, merge_format4_bold,
                           '七、验收标准及提出异议时间：', self.c.get_yanshou())
        sheet1.merge_range(f'A{row + 8}:H{row + 9}', '八、标的物所有权自供方收到货款之日起转移给需方，在需方未履行（支付款项/100%货款）义务前，'
                                                     '标的物仍属于供方所有，标的物毁损，灭失等风险自交付时起由需方承担。', merge_format4)
        write_nonbold_bold(sheet1, f'A{row + 10}:H{row + 10}', merge_format4, merge_format4_bold,
                           '九、结算方式及期限：', self.c.get_jiesuan())
        write_nonbold_bold(sheet1, f'A{row + 11}:H{row + 11}', merge_format4, merge_format4_bold,
                           '十、如需提供担保，另立合同担保书，作为本合同附件：', self.c.get_ruxu())
        write_nonbold_bold(sheet1, f'A{row + 12}:H{row + 12}', merge_format4, merge_format4_bold,
                           '十一、违约责任：', self.c.get_weiyue())
        write_nonbold_bold(sheet1, f'A{row + 13}:H{row + 13}', merge_format4, merge_format4_bold,
                           '十二、解决合同纠纷的方式：', self.c.get_jiejue())
        row += 13
        write_nonbold_bold(sheet1, f'A{row + 1}:H{row + 1}', merge_format4, merge_format4_bold,
                           '十三、其它约定事情:', self.c.get_qita())
        row += 2
        sheet1.merge_range(f'A{row + 1}:C{row + 1}', '供方', format1_left_top)
        sheet1.merge_range(f'D{row + 1}:H{row + 1}', '需方', format1_right_top)
        row += 1
        supplier_info = self.c.get_supplier_info()
        buyer_info = self.c.get_buyer_info()
        write_nonbold_bold(sheet1, f'A{row + 1}:C{row + 1}', merge_format4, merge_format4,
                           '单位名称（章）：', supplier_info[0], left)
        write_nonbold_bold(sheet1, f'D{row + 1}:H{row + 1}', merge_format4, merge_format4,
                           '单位名称（章）：', buyer_info[0], right)
        write_nonbold_bold(sheet1, f'A{row + 2}:C{row + 2}', merge_format4, merge_format4,
                           '单位地址：', supplier_info[1], left)
        write_nonbold_bold(sheet1, f'D{row + 2}:H{row + 2}', merge_format4, merge_format4,
                           '单位地址：', buyer_info[1], right)
        sheet1.merge_range(f'A{row + 3}:C{row + 3}', '法定代表人：', left)
        sheet1.merge_range(f'D{row + 3}:H{row + 3}', '法定代表人：', right)
        sheet1.merge_range(f'A{row + 4}:C{row + 4}', '委托代表人：', left)
        sheet1.merge_range(f'D{row + 4}:H{row + 4}', '委托代表人：', right)
        sheet1.merge_range(f'A{row + 5}:C{row + 5}', '签字日期：', left)
        sheet1.merge_range(f'D{row + 5}:H{row + 5}', '签字日期：', right)
        write_nonbold_bold(sheet1, f'A{row + 6}:C{row + 6}', merge_format4, merge_format4,
                           '开户银行', supplier_info[2], left)
        write_nonbold_bold(sheet1, f'D{row + 6}:H{row + 6}', merge_format4, merge_format4,
                           '开户银行：', buyer_info[2], right)
        write_nonbold_bold(sheet1, f'A{row + 7}:C{row + 7}', merge_format4, merge_format4,
                           '帐号：', supplier_info[3], left)
        write_nonbold_bold(sheet1, f'D{row + 7}:H{row + 7}', merge_format4, merge_format4,
                           '帐号：', buyer_info[3], right)
        write_nonbold_bold(sheet1, f'A{row + 8}:C{row + 8}', merge_format4, merge_format4,
                           '税证号码：', supplier_info[4], left)
        write_nonbold_bold(sheet1, f'D{row + 8}:H{row + 8}', merge_format4, merge_format4,
                           '税证号码：', buyer_info[4], right)
        write_nonbold_bold(sheet1, f'A{row + 9}:C{row + 9}', merge_format4, merge_format4,
                           '电话：', supplier_info[5], left_bottom)
        write_nonbold_bold(sheet1, f'D{row + 9}:H{row + 9}', merge_format4,
                           merge_format4, '电话：', buyer_info[5], right_bottom) # todo
        sheet1.insert_image(f'A{row + 2}', 'data\\stamp1.png', {'x_offset': 40})

        for i in range(1, row + 11):
            sheet1.set_row(i, 20)

        # sheet2
        sheet2 = workbook.add_worksheet('合同清单')
        sheet2.set_row(0, 30)
        sheet2.set_column(0, 0, 5)
        sheet2.set_column(1, 1, 15)
        sheet2.set_column(2, 2, 30)
        sheet2.set_column(3, 10, 10)

        sheet2.merge_range('A1:K1', '购销合同清单', merge_format1)
        sheet2.merge_range('A2:K2', f'合同编号：{self.c.get_contract_num()}', merge_format2)

        for col in range(11):
            sheet2.write(2, col, ['序号', '产品名称', '型号及规格', '单位', '数量', '面价', '折扣',
                                  '附件', '单价', '金额', '备注'][col], format1_bold)
        row, col = 3, 0
        for product_id, number, discount in self.c.get_table():
            product = self.dl.get_product(product_id)
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
        sheet2.merge_range(f'A{row + 2}:K{row + 2}', f'合计人民币金额（大写）：{self.c.get_total_daxie()}', merge_format3)
        write_nonbold_bold(sheet2, f'A{row + 4}:D{row + 4}', merge_format4, merge_format4_bold, '单位名称（章）：',
                           c.get_supplier())
        write_nonbold_bold(sheet2, f'E{row + 4}:K{row + 4}', merge_format4, merge_format4_bold, '单位名称（章）：',
                           c.get_buyer())
        sheet2.merge_range(f'A{row + 6}:D{row + 6}', '日期：', merge_format4)
        sheet2.merge_range(f'E{row + 6}:K{row + 6}', '日期：', merge_format4)
        sheet2.insert_image(f'B{row + 1}', 'data\\stamp1.png')
        for i in range(2, row + 7):
            sheet2.set_row(i, 20)
        workbook.close()


def write_nonbold_bold(sheet, mRange, format_nonbold, format_bold, s1, s2, merge_format=None):
    if not merge_format:
        sheet.merge_range(mRange, None, format_nonbold)
        sheet.write_rich_string(mRange[:mRange.find(':')], format_nonbold, s1, format_bold, s2)
    else:
        sheet.merge_range(mRange,None, merge_format)
        sheet.write_rich_string(mRange[:mRange.find(':')], format_nonbold, s1, format_bold, s2, merge_format)



if __name__ == '__main__':
    os.chdir('../')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING)
    dl = DataLoader()
    dl.load()

    c = Contract(dl, '中山市湘华电力科技有限公司', '广州')
    c.add_item(1, 20, 0.8)
    c.add_item(0, 10, 0.9)

    test = Excel(c, dl)
    test.run()
