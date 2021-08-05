from child_window import ChildWindow
from dataLoader import DataLoader
from warning_window import WarningWindow
from setting_window import SettingWindow
import tkinter
import tkinter.ttk
import tkinter.filedialog

product_type = {'框架断路器': ['RMW1', 'RMW2', 'ME', 'RMW3'],
                '塑壳断路器': ['RMM1', 'RMM2', 'RMM3', 'RMM1L', 'RMM2L', 'RMM3L', 'RMM3D'],
                '小型断路器': ['RMGQ', 'RMC3', 'RMC5', 'RMC3E'],
                '交流接触器': ['B', 'RMK', 'CJ20', 'CJ40', 'BC', 'RMKC'],
                '高压真空断路器': ['RMVS1', 'RMV1'],
                '起动器': ['MSB', 'RMS1', 'RMD2', 'RMS2'],
                '自动转换开关': ['RMQ1', 'RMQ3', 'RMQ6', 'RMQ5Y', 'RMQ6G'],
                '其他产品': ['CA', 'CK', 'VB', 'VK', 'T联接板', 'T背包', '单供附件', 'P1700', 'NT'],
                '热继电器': ['T'],
                '特种电器': ['RMU1', 'RMG1', 'RMMG1', 'RMU3', 'RMKB1']}


class ContractWindow(ChildWindow):
    pass
    contract_window_count = 0

    def __init__(self, master, cid, data_loader, contract_loader):
        self.cid = cid
        self.master = master
        self.data_loader = data_loader
        self.contract_loader = contract_loader
        self.library_chosen_pid = None
        if self.check():
            self.master.withdraw()
        super().__init__(master, 1600, 900, 1600, 800, True)

    def close(self):
        __class__.contract_window_count -= 1
        self.master.deiconify()
        self.contract_loader.save(self.cid)
        super().close()

    @staticmethod
    def check():
        return __class__.contract_window_count < 1

    def gui_init(self, window):
        __class__.contract_window_count += 1

        widget_list = dict()
        self.data["widget_list"] = widget_list

        library_frame = tkinter.Frame(self.window, bg="#262626")
        tkinter.Frame(library_frame, bg="#464646", width=3).pack(side="right", fill="y")
        tkinter.Frame(library_frame, bg="#262626", width=15).pack(side="left", fill="y")
        tkinter.Frame(library_frame, bg="#262626", width=15).pack(side="right", fill="y")
        tkinter.Frame(library_frame, bg="#262626", height=15).pack(side="top", fill="x")
        tkinter.Frame(library_frame, bg="#262626", height=15).pack(side="bottom", fill="x")
        library_frame.place(relwidth=0.3, relheight=1)

        contract_frame = tkinter.Frame(self.window, bg="#323232")
        contract_frame.place(relwidth=0.7, relheight=1, relx=0.3)

        library_chosen_frame = tkinter.Frame(library_frame, bg="#262626", padx=10, pady=10, height=400)
        library_chosen_frame.pack(side="top", fill="x")

        # 产品库中选中产品的信息布局
        chosen_line_01 = tkinter.Frame(library_chosen_frame, bg="#262626", pady=3)
        chosen_name_01 = tkinter.Label(chosen_line_01, bg="#262626", text="产品名:  ", fg="#9A9A9A")
        chosen_name_02 = tkinter.Label(chosen_line_01, bg="#262626", text="<未选择>", fg="#E4E4E4")
        chosen_line_02 = tkinter.Frame(library_chosen_frame, bg="#262626", pady=3)
        chosen_type_01 = tkinter.Label(chosen_line_02, bg="#262626", text="型号规格:", fg="#9A9A9A")
        chosen_type_02 = tkinter.Label(chosen_line_02, bg="#262626", text="<未选择>", fg="#E4E4E4")
        chosen_line_03 = tkinter.Frame(library_chosen_frame, bg="#262626", pady=3)
        chosen_adjunct01_frame = tkinter.Frame(chosen_line_03, bg="#262626")
        chosen_adjunct_01 = tkinter.Label(chosen_adjunct01_frame, bg="#262626", text="附加:    ", fg="#9A9A9A")
        chosen_adjunct_02 = tkinter.Text(chosen_line_03, bg="#262626", fg="#E4E4E4", height=3, bd=0)
        chosen_adjunct_02.insert("1.0", "<未选择>")
        chosen_adjunct_02.configure(state="disabled")
        chosen_line_04 = tkinter.Frame(library_chosen_frame, bg="#262626", pady=3)
        chosen_price_01 = tkinter.Label(chosen_line_04, bg="#262626", text="面价:    ", fg="#9A9A9A")
        chosen_price_02 = tkinter.Label(chosen_line_04, bg="#262626", text="<未选择>", fg="#E4E4E4")
        chosen_line_05 = tkinter.Frame(library_chosen_frame, bg="#262626", pady=3)
        chosen_adjunctPrice_01 = tkinter.Label(chosen_line_05, bg="#262626", text="附加价格:", fg="#9A9A9A")
        chosen_adjunctPrice_02 = tkinter.Label(chosen_line_05, bg="#262626", text="<未选择>", fg="#E4E4E4")
        chosen_name_01.pack(side="left")
        chosen_name_02.pack(side="left")
        chosen_line_01.pack(side="top", fill="x")
        chosen_type_01.pack(side="left")
        chosen_type_02.pack(side="left")
        chosen_line_02.pack(side="top", fill="x")
        chosen_adjunct01_frame.pack(side="left", fill="y")
        chosen_adjunct_01.pack(side="top")
        chosen_adjunct_02.pack(side="left", fill="x")
        chosen_line_03.pack(side="top", fill="x")
        chosen_price_01.pack(side="left")
        chosen_price_02.pack(side="left")
        chosen_line_04.pack(side="top", fill="x")
        chosen_adjunctPrice_01.pack(side="left")
        chosen_adjunctPrice_02.pack(side="left")
        chosen_line_05.pack(side="top", fill="x")

        chosen_line_06 = tkinter.Frame(library_chosen_frame, bg="#363636", pady=10, padx=10)
        product_add_button = tkinter.Label(chosen_line_06, text="添加", padx=20, cursor="hand2", fg="#E4E4E4",
                                           bg="#649AFA")
        amount_line = tkinter.Frame(chosen_line_06, bg="#363636")
        amount_label = tkinter.Label(amount_line, bg="#363636", fg="#9A9A9A", text="数量:")
        amount_entry = tkinter.Text(amount_line, bg="#646464", fg="#A0A0A0",
                                    highlightbackground="#A0A0A0",
                                    highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                    insertbackground="#A0A0A0",
                                    height=1, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        discount_line = tkinter.Frame(chosen_line_06, bg="#363636")
        discount_label = tkinter.Label(discount_line, bg="#363636", fg="#9A9A9A", text="折扣:")
        discount_entry = tkinter.Text(discount_line, bg="#646464", fg="#A0A0A0",
                                      highlightbackground="#A0A0A0",
                                      highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                      insertbackground="#A0A0A0",
                                      height=1, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        comments_line = tkinter.Frame(chosen_line_06, bg="#363636")
        comments_label = tkinter.Label(comments_line, bg="#363636", fg="#9A9A9A", text="备注:")
        comments_entry = tkinter.Text(comments_line, bg="#646464", fg="#A0A0A0",
                                      highlightbackground="#A0A0A0",
                                      highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                      insertbackground="#A0A0A0",
                                      height=1, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        product_add_button.pack(side="right", fill="y")
        tkinter.Frame(chosen_line_06, width=15, bg="#363636").pack(side="right", fill="y")
        amount_label.pack(side="left")
        amount_entry.pack(side="left", fill="x")
        amount_line.pack(side="top", fill="x")
        tkinter.Frame(chosen_line_06, height=10, bg="#363636").pack(side="top", fill="x")
        discount_label.pack(side="left")
        discount_entry.pack(side="left", fill="x")
        discount_line.pack(side="top", fill="x")
        tkinter.Frame(chosen_line_06, height=10, bg="#363636").pack(side="top", fill="x")
        comments_label.pack(side="left")
        comments_entry.pack(side="left", fill="x")
        comments_line.pack(side="top", fill="x")
        chosen_line_06.pack(side="top", fill="x")

        product_add_button.bind("<Enter>", self.button_enter)
        product_add_button.bind("<Leave>", self.button_leave)

        widget_list["amount_entry"] = amount_entry
        widget_list["discount_entry"] = discount_entry
        widget_list["comments_entry"] = comments_entry

        # 以下是产品库布局
        combobox_font = ('黑体', '14')
        self.window.option_add("*TCombobox*Listbox.font", combobox_font)
        self.window.option_add("*TCombobox*Listbox.background", "#464646")
        self.window.option_add("*TCombobox*Listbox.foreground", "#E4E4E4")
        self.window.option_add("*TCombobox*Listbox.selectBackground", "#649AFA")

        library_detail_frame = tkinter.Frame(library_frame, bg="#363636", padx=10, pady=10)
        search_image = tkinter.PhotoImage(file="img/search_icon.png", width=35, height=35)
        self.data["search_image"] = search_image
        product_detail_line01 = tkinter.Frame(library_detail_frame, bg="#363636")
        product_screen_label01 = tkinter.Label(product_detail_line01, bg="#363636", fg="#A0A0A0", text="产品名称:")
        screen_name_cb = tkinter.ttk.Combobox(product_detail_line01, state="readonly", font=combobox_font, width=14)
        keys = list(product_type.keys())
        keys.insert(0, "全部")
        screen_name_cb["value"] = tuple(keys)
        screen_name_cb.current(0)
        product_screen_label02 = tkinter.Label(product_detail_line01, bg="#363636", fg="#A0A0A0", text="型号:")
        screen_type_cb = tkinter.ttk.Combobox(product_detail_line01, state="readonly", font=combobox_font, width=8)
        screen_type_cb["value"] = tuple(["全部"])
        screen_type_cb.current(0)
        product_detail_line02 = tkinter.Frame(library_detail_frame, bg="#363636")
        product_search_label = tkinter.Label(product_detail_line02, text="搜索:",  bg="#363636", fg="#A0A0A0")
        product_search_entry = tkinter.Text(product_detail_line02, bg="#646464", fg="#A0A0A0",
                                            highlightbackground="#A0A0A0",
                                            highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                            insertbackground="#A0A0A0",
                                            height=1, wrap="none", undo=True, maxundo=-1, padx=10,
                                            pady=5)

        product_screen_label01.pack(side="left")
        screen_name_cb.pack(side="left")
        tkinter.Frame(product_detail_line01, bg="#363636", width=5).pack(side="left")
        product_screen_label02.pack(side="left")
        screen_type_cb.pack(side="left")
        product_detail_line01.pack(side="top", fill="x")
        tkinter.Frame(library_detail_frame, bg="#363636", height=10).pack(side="top")
        product_search_label.pack(side="left")
        product_search_entry.pack(side="left", fill="x")
        product_detail_line02.pack(side="top", fill="x")
        tkinter.Frame(library_detail_frame, bg="#363636", height=10).pack(side="top")
        library_detail_frame.pack(side="top", fill="both", expand=1)

        columns = ("name", "type", "price")
        product_library = tkinter.ttk.Treeview(library_detail_frame, show="headings", select="browse",
                                               columns=columns, style="Custom.Treeview")
        product_library.heading("name", text="产品名称")
        product_library.heading("type", text="型号及规格")
        product_library.heading("price", text="面价")
        product_library.column("name", width=130, anchor="w")
        product_library.column("type", width=150, anchor="w")
        product_library.column("price", width=80, anchor="w")

        product_library_scroll = tkinter.Scrollbar(library_detail_frame, command=product_library.yview)
        product_library.configure(yscrollcommand=product_library_scroll.set)

        product_library_scroll.pack(side="right", fill="y")
        product_library.pack(side="top", expand=1, fill="both")

        def library_select(evt):
            selection = self.select(evt.widget)
            if len(selection) > 0:
                chosen_pid = int(selection[0])
                chosen_product = self.data_loader.get_product(chosen_pid)
                name = chosen_product.get_name()
                model = chosen_product.get_model()
                price = chosen_product.get_raw_price()
                adjunct = chosen_product.get_adjunct()
                adjunct_price = chosen_product.get_adjunct_price()
                chosen_name_02.config(text=name)
                chosen_type_02.config(text=model)
                chosen_price_02.config(text="%s元" % price)
                chosen_adjunct_02.configure(state="normal")
                chosen_adjunct_02.delete("1.0", "end")
                chosen_adjunct_02.insert("1.0", adjunct)
                chosen_adjunct_02.configure(state="disabled")
                chosen_adjunctPrice_02.config(text="%s元" % adjunct_price)
                self.library_chosen_pid = chosen_pid
            else:
                chosen_name_02.config(text="<未选择>")
                chosen_type_02.config(text="<未选择>")
                chosen_price_02.config(text="<未选择>")
                chosen_adjunct_02.configure(state="normal")
                chosen_adjunct_02.delete("1.0", "end")
                chosen_adjunct_02.insert("1.0", "<未选择>")
                chosen_adjunct_02.configure(state="disabled")
                chosen_adjunctPrice_02.config(text="<未选择>")
                self.library_chosen_pid = None

        def to_search(evt):
            self.search()
            return "break"

        product_library.bind('<<TreeviewSelect>>', library_select)

        screen_name_cb.bind("<<ComboboxSelected>>", self.screen_name_change)
        screen_type_cb.bind("<<ComboboxSelected>>", to_search)
        product_search_entry.bind("<Return>", to_search)

        widget_list["screen_name_cb"] = screen_name_cb
        widget_list["screen_type_cb"] = screen_type_cb
        widget_list["product_search_entry"] = product_search_entry
        widget_list["product_library"] = product_library

        self.products_read()

        # 以下为右侧布局
        contract = self.contract_loader.get(self.cid)
        contract_name = contract[-2]
        contract_number = contract[-1]
        contract_type = "合同" if len(self.cid) == 8 else "报价单"

        top_info_frame = tkinter.Frame(contract_frame, bg="#323232")
        top_info_frame.pack(side="top", fill="x")
        tkinter.Frame(top_info_frame, bg="#464646", height=3).pack(side="bottom", fill="x")
        tkinter.Frame(top_info_frame, bg="#323232", height=10).pack(side="bottom", fill="x")
        tkinter.Frame(top_info_frame, bg="#323232", height=10).pack(side="top", fill="x")
        tkinter.Frame(top_info_frame, bg="#323232", width=15).pack(side="left", fill="y")
        tkinter.Frame(top_info_frame, bg="#323232", width=10).pack(side="right", fill="y")
        info_type_label = tkinter.Label(top_info_frame, bg="#464646", fg="#9A9A9A", padx=10, pady=5,
                                        text=contract_type)
        info_number_label = tkinter.Label(top_info_frame, bg="#464646", fg="#9A9A9A", padx=10, pady=5,
                                          text=contract_number)
        info_name_label = tkinter.Label(top_info_frame, bg="#323232", fg="#A0A0A0", text=contract_name)
        setting_img = tkinter.PhotoImage(file="img/setting_icon.png", width=35, height=35)
        self.data["setting_img"] = setting_img
        info_setting_button = tkinter.Label(top_info_frame, image=setting_img, bg="#323232", cursor="hand2")

        def setting_recall():
            self.search()

        def open_setting(evt):
            setting_menu = SettingWindow(master=self.window, width=1280, height=800, resizable=True, title="设置",
                                         data_loader=self.data_loader, command=setting_recall)

        info_setting_button.bind("<Button-1>", open_setting)

        info_type_label.pack(side="left")
        tkinter.Frame(top_info_frame, bg="#323232", width=10).pack(side="left")
        info_number_label.pack(side="left")
        tkinter.Frame(top_info_frame, bg="#323232", width=15).pack(side="left")
        info_name_label.pack(side="left")
        info_setting_button.pack(side="right")
        tkinter.Frame(top_info_frame, bg="#323232", width=15).pack(side="left")

        info_bottom_line = tkinter.Frame(contract_frame, bg="#323232", padx=10, pady=5)
        contract_export = tkinter.Label(info_bottom_line, bg="#649AFA", fg="#E4E4E4", text="导出为...",
                                        cursor="hand2", padx=8, pady=4, font="黑体 14")
        product_list_delete = tkinter.Label(info_bottom_line, bg="#646464", fg="#A0A0A0", text="移除选中产品",
                                            cursor="arrow", padx=8, pady=4, font="黑体 14")

        lock_image = tkinter.PhotoImage(file="img/lock_icon.png", width=35, height=35)
        unlock_image = tkinter.PhotoImage(file="img/unlock_icon.png", width=35, height=35)
        self.data["lock_image"] = lock_image
        self.data["unlock_image"] = unlock_image
        self.data["delete_lock"] = True
        product_delete_lock = tkinter.Label(info_bottom_line, bg="#323232", image=lock_image, cursor="hand2")

        total_label = tkinter.Label(info_bottom_line, bg="#323232", fg="#9A9A9A", text="合计数量:-  合计金额:-")
        widget_list["total_label"] = total_label

        contract_export.pack(side="right")
        tkinter.Frame(info_bottom_line, bg="#323232", width=10).pack(side="right")
        product_list_delete.pack(side="right")
        product_delete_lock.pack(side="right")
        total_label.pack(side="left")
        info_bottom_line.pack(side="bottom", fill="x")

        widget_list["product_list_delete"] = product_list_delete
        widget_list["product_delete_lock"] = product_delete_lock

        product_delete_lock.bind("<Button-1>", self.lock_change)
        contract_export.bind("<Enter>", self.button_enter)
        contract_export.bind("<Leave>", self.button_leave)

        columns = ("number", "name", "model", "unit", "amount", "price", "discount", "adjunctPrice", "singlePrice",
                   "totalPrice", "comments")
        contract_product = tkinter.ttk.Treeview(contract_frame, show="headings", columns=columns, style="Custom.Treeview")
        contract_product.heading("number", text="序号")
        contract_product.heading("name", text="产品名称")
        contract_product.heading("model", text="型号及规格")
        contract_product.heading("unit", text="单位")
        contract_product.heading("amount", text="数量")
        contract_product.heading("price", text="面价")
        contract_product.heading("discount", text="折扣")
        contract_product.heading("adjunctPrice", text="附件")
        contract_product.heading("singlePrice", text="单价")
        contract_product.heading("totalPrice", text="金额")
        contract_product.heading("comments", text="备注")

        contract_product.column("number", width=30, anchor="center")
        contract_product.column("name", width=130, anchor="w")
        contract_product.column("model", width=330, anchor="w")
        contract_product.column("unit", width=40, anchor="center")
        contract_product.column("amount", width=40, anchor="center")
        contract_product.column("price", width=80, anchor="center")
        contract_product.column("discount", width=60, anchor="center")
        contract_product.column("adjunctPrice", width=60, anchor="center")
        contract_product.column("singlePrice", width=80, anchor="center")
        contract_product.column("totalPrice", width=80, anchor="center")
        contract_product.column("comments", width=80, anchor="w")

        contract_library_scroll = tkinter.Scrollbar(contract_frame, command=contract_product.yview)
        contract_product.configure(yscrollcommand=contract_library_scroll.set)

        contract_library_scroll.pack(side="right", fill="y")
        contract_product.pack(side="left", fill="both", expand=1)

        widget_list["contract_product"] = contract_product

        def contract_product_select(evt):
            self.select(contract_product)

        contract_product.bind('<<TreeviewSelect>>', contract_product_select)
        self.contract_product_refresh()

        product_add_button.bind("<Button-1>", self.add_product)

        def export_as_contract():
            file_path = tkinter.filedialog.asksaveasfilename(title=u'保存合同', filetypes=[("excel表格", ".xlsx")],
                                                             initialfile=contract_number + contract_name,
                                                             parent=window)
            self.contract_loader.export_excel(self.cid, 0, file_path)

        def export_as_quotation():
            file_path = tkinter.filedialog.asksaveasfilename(title=u'保存报价单', filetypes=[("excel表格", ".xlsx")],
                                                             initialfile=contract_number + contract_name,
                                                             parent=window)
            self.contract_loader.export_excel(self.cid, 0, file_path)

        def export_as_pdf():
            warning_window = WarningWindow(master=self.window, text="此功能还在开发中。")

        def menu_show(evt):
            x = evt.x_root
            y = evt.y_root
            item_menu.post(x, y)

        item_menu = tkinter.Menu(window, tearoff=False, font="新宋体 13", bg="#262626", fg="#A0A0A0")
        if len(self.cid) == 8:
            item_menu.add_command(label="导出为excel表格", command=export_as_contract)
        elif len(self.cid) == 10:
            item_menu.add_command(label="导出为excel表格", command=export_as_quotation)
            item_menu.add_command(label="导出为pdf文件", command=export_as_pdf)
        item_menu.place()

        contract_export.bind("<Button-1>", menu_show)

    @staticmethod
    def button_enter(evt):
        evt.widget.config(bg="#84AAFF")

    @staticmethod
    def button_leave(evt):
        evt.widget.config(bg="#649AFA")

    @staticmethod
    def select(widget):
        tree_view = widget
        selection = tree_view.selection()
        for i in tree_view.get_children():
            if i in selection:
                tree_view.tag_configure(i, background="#649AFA", foreground="#E4E4E4")
            else:
                tree_view.tag_configure(i, background="#323232", foreground="#A0A0A0")
        return selection

    def add_product(self, evt):
        if self.library_chosen_pid is not None:
            amount = self.data["widget_list"]["amount_entry"].get("1.0", "end-1c")
            discount = self.data["widget_list"]["discount_entry"].get("1.0", "end-1c")
            comments = self.data["widget_list"]["comments_entry"].get("1.0", "end-1c")
            product = self.data_loader.get_product(self.library_chosen_pid)
            result = self.contract_loader.add_product(self.cid, product, amount, discount, comments)
            if result == 1:
                warning_window = WarningWindow(master=self.window, text="数量必须为正整数。")
                return
            elif result == 2:
                warning_window = WarningWindow(master=self.window, text="折扣格式错误，输入范围为0~1。")
                return
            elif result == 3:
                warning_window = WarningWindow(master=self.window, text="产品已添加，\n如需修改请先移除原有产品。")
                return
            elif result == 0:
                self.contract_product_refresh()
                self.data["widget_list"]["amount_entry"].delete("1.0", "end")
                self.data["widget_list"]["discount_entry"].delete("1.0", "end")
                self.data["widget_list"]["comments_entry"].delete("1.0", "end")

    def contract_product_refresh(self):
        product_list = self.contract_loader.get_table_info(self.cid)
        contract_product = self.data["widget_list"]["contract_product"]
        for i in contract_product.get_children():
            contract_product.delete(i)
        for i in range(len(product_list)):
            id_tag = str(i)
            contract_product.insert('', i, values=product_list[i], tags=(id_tag, "all"), iid=id_tag)

        total = self.contract_loader.get_table_total(self.cid)
        self.select(contract_product)
        self.data["widget_list"]["total_label"].config(text="合计数量:%s  合计金额:%s" % (total[0], total[1]))

    def delete_product(self, evt):
        contract_product = self.data["widget_list"]["contract_product"]
        selection = list(contract_product.selection())
        selection.reverse()
        for i in selection:
            self.contract_loader.remove_product(self.cid, int(i))
        self.contract_product_refresh()
        self.lock_change(None)

    def lock_change(self, evt):
        if self.data["delete_lock"]:
            self.data["widget_list"]["product_delete_lock"].configure(image=self.data["unlock_image"])
            self.data["widget_list"]["product_list_delete"].configure(bg="#649AFA", fg="#E4E4E4", cursor="hand2")
            self.data["widget_list"]["product_list_delete"].bind("<Enter>", self.button_enter)
            self.data["widget_list"]["product_list_delete"].bind("<Leave>", self.button_leave)
            self.data["widget_list"]["product_list_delete"].bind("<Button-1>", self.delete_product)
        else:
            self.data["widget_list"]["product_delete_lock"].configure(image=self.data["lock_image"])
            self.data["widget_list"]["product_list_delete"].configure(bg="#646464", fg="#A0A0A0", cursor="arrow")
            self.data["widget_list"]["product_list_delete"].unbind("<Enter>")
            self.data["widget_list"]["product_list_delete"].unbind("<Leave>")
            self.data["widget_list"]["product_list_delete"].unbind("<Button-1>")
        self.data["delete_lock"] = not self.data["delete_lock"]

    def product_library_set(self, name_list, type_list, price_list, pid_list):
        self.data["pid_list"] = pid_list
        # product_id_list = list()
        for i in range(len(name_list)):
            id_tag = str(pid_list[i])
            # product_id_list.append(id_tag)
            self.data["widget_list"]["product_library"].insert('', i,
                                                               values=(name_list[i], type_list[i], price_list[i]),
                                                               tags=(id_tag, "all"), iid=id_tag)
        # self.data["product_id_list"] = product_id_list

    def product_load(self, product_list):
        for i in self.data["widget_list"]["product_library"].get_children():
            self.data["widget_list"]["product_library"].delete(i)
        name_list = list()
        type_list = list()
        price_list = list()
        pid_list = list()
        for i in product_list:
            pid_list.append(i[0])
            product = i[1]
            name_list.append(product.get_name())
            type_list.append(product.get_model())
            price_list.append(product.get_raw_price())
        self.product_library_set(name_list, type_list, price_list, pid_list)

    def products_read(self):
        data_loader = self.data_loader
        self.product_load(data_loader.get_products_list())

    def search(self):
        name = self.data["widget_list"]["screen_name_cb"].get()
        type = self.data["widget_list"]["screen_type_cb"].get()
        name = None if name == "全部" else name
        type = None if type == "全部" else type
        keyword = self.data["widget_list"]["product_search_entry"].get("1.0", 'end-1c')
        data_loader = self.data_loader
        product_list = DataLoader.search(data_loader.get_products_list(), name, type, keyword)
        self.product_load(product_list)

    def screen_name_change(self, evt):
        choice = self.data["widget_list"]["screen_name_cb"].get()
        keys = list(product_type[choice]) if choice != "全部" else list()
        keys.insert(0, "全部")
        self.data["widget_list"]["screen_type_cb"]["value"] = keys
        self.data["widget_list"]["screen_type_cb"].current(0)
        self.search()
