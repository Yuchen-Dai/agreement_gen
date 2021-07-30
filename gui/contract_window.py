from child_window import ChildWindow
from dataLoader import DataLoader
from warning_window import WarningWindow
import tkinter
import tkinter.ttk

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
        super().close()

    @staticmethod
    def check():
        return __class__.contract_window_count < 1

    def gui_init(self, window):
        __class__.contract_window_count += 1
        try:
            combostyle = tkinter.ttk.Style()
            combostyle.theme_create('combostyle', parent='clam',
                                    settings={'TCombobox':
                                                  {'configure':
                                                       {'selectbackground': '#646464',
                                                        'fieldbackground': '#646464',
                                                        'background': '#646464',
                                                        'foreground': "#A0A0A0",
                                                        'arrowsize': 15,
                                                        'lightcolor': "#646464",
                                                        'arrowcolor': "#A0A0A0",
                                                        'selectforeground': "#929292",
                                                        'padding': 6
                                                        }}}
                                    )
            combostyle.theme_use('combostyle')

            style = tkinter.ttk.Style()
            style.element_create("Custom.Treeheading.border", "from", "default")
            style.layout("Custom.Treeview.Heading", [
                ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
                ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                        ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                        ("Custom.Treeheading.text", {'sticky': 'we'})
                    ]})
                ]}),
            ])
            head_font = ('黑体', '12')
            content_font = ('宋体', '12')
            style.configure("Custom.Treeview.Heading",
                            background="#646464", foreground="#E4E4E4", relief="flat", font=head_font)
            style.configure("Custom.Treeview", background="#323232", foreground="#A0A0A0", fieldbackground="#323232",
                            highlightthickness=0, font=content_font)
            style.map("Custom.Treeview.Heading",
                      relief=[('active', 'groove'), ('pressed', 'sunken')])
        except BaseException:
            print("主题已添加")

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
        contract = self.contract_loader.get_contract(self.cid)
        contract_name = contract[-2]
        contract_number = contract[-1]

        top_info_frame = tkinter.Frame(contract_frame, bg="#323232")
        top_info_frame.pack(side="top", fill="x")
        tkinter.Frame(top_info_frame, bg="#464646", height=3).pack(side="bottom", fill="x")
        tkinter.Frame(top_info_frame, bg="#323232", height=10).pack(side="bottom", fill="x")
        tkinter.Frame(top_info_frame, bg="#323232", height=10).pack(side="top", fill="x")
        tkinter.Frame(top_info_frame, bg="#323232", width=15).pack(side="left", fill="y")
        tkinter.Frame(top_info_frame, bg="#323232", width=10).pack(side="right", fill="y")
        info_number_label = tkinter.Label(top_info_frame, bg="#464646", fg="#9A9A9A", padx=10, pady=5,
                                          text=contract_number)
        info_name_label = tkinter.Label(top_info_frame, bg="#323232", fg="#A0A0A0", text=contract_name)
        setting_img = tkinter.PhotoImage(file="img/setting_icon.png", width=35, height=35)
        self.data["setting_img"] = setting_img
        info_setting_button = tkinter.Label(top_info_frame, image=setting_img, bg="#323232", cursor="hand2")

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
        contract_product = tkinter.ttk.Treeview(contract_frame, show="headings", select="browse",
                                                columns=columns, style="Custom.Treeview")
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

        contract_product.column("number", width=30, anchor="w")
        contract_product.column("name", width=130, anchor="w")
        contract_product.column("model", width=330, anchor="w")
        contract_product.column("unit", width=40, anchor="w")
        contract_product.column("amount", width=40, anchor="w")
        contract_product.column("price", width=80, anchor="w")
        contract_product.column("discount", width=60, anchor="w")
        contract_product.column("adjunctPrice", width=60, anchor="w")
        contract_product.column("singlePrice", width=80, anchor="w")
        contract_product.column("totalPrice", width=80, anchor="w")
        contract_product.column("comments", width=80, anchor="w")

        contract_library_scroll = tkinter.Scrollbar(contract_frame, command=contract_product.yview)
        contract_product.configure(yscrollcommand=contract_library_scroll.set)

        contract_library_scroll.pack(side="right", fill="y")
        contract_product.pack(side="left", fill="both", expand=1)

        widget_list["contract_product"] = contract_product
        self.contract_product_refresh()

        product_add_button.bind("<Button-1>", self.add_product)

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

    def contract_product_refresh(self):
        product_list = self.contract_loader.get_table_info(self.cid)
        contract_product = self.data["widget_list"]["contract_product"]
        for i in contract_product.get_children():
            contract_product.delete(i)
        for i in range(len(product_list)):
            contract_product.insert('', i, values=product_list[i], tags=(i, "all"), iid=i)

    def delete_product(self, evt):
        pass

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

# import tkinter
# import tkinter.ttk
# import re
# from child_window import ChildWindow
# from warning_window import WarningWindow
# from assembly import StandardBar
# from dataLoader import DataLoader
# from excel import Excel
# from contract import Contract
# from product import Product
#
# product_type = {'框架断路器': ['RMW1', 'RMW2', 'ME', 'RMW3'],
#                 '塑壳断路器': ['RMM1', 'RMM2', 'RMM3', 'RMM1L', 'RMM2L', 'RMM3L', 'RMM3D'],
#                 '小型断路器': ['RMGQ', 'RMC3', 'RMC5', 'RMC3E'],
#                 '交流接触器': ['B', 'RMK', 'CJ20', 'CJ40', 'BC', 'RMKC'],
#                 '高压真空断路器': ['RMVS1', 'RMV1'],
#                 '起动器': ['MSB', 'RMS1', 'RMD2', 'RMS2'],
#                 '自动转换开关': ['RMQ1', 'RMQ3', 'RMQ6', 'RMQ5Y', 'RMQ6G'],
#                 '其他产品': ['CA', 'CK', 'VB', 'VK', 'T联接板', 'T背包', '单供附件', 'P1700', 'NT'],
#                 '热继电器': ['T'],
#                 '特种电器': ['RMU1', 'RMG1', 'RMMG1', 'RMU3', 'RMKB1']}
#
#
# class ContractWindow(ChildWindow):
#     setting_count = 0
#
#     @staticmethod
#     def check():
#         return __class__.setting_count < 1
#
#     def close(self):
#         __class__.setting_count -= 1
#         super().close()
#
#     def gui_init(self, window):
#         __class__.setting_count += 1
#         menu_frame = tkinter.Frame(self.window, bg="#262626", bd=0)
#         menu_frame.place(width=160, relheight=1)
#
#         choice_001 = tkinter.Label(menu_frame, bg="#262626", text="基础设置", fg="#9A9A9A", height=3, cursor="hand2")
#         choice_001.pack(fill="x", side="top")
#         choice_002 = tkinter.Label(menu_frame, bg="#262626", text="产品管理", fg="#649AFA", height=3, cursor="hand2")
#         choice_002.pack(fill="x", side="top")
#         choice_003 = tkinter.Label(menu_frame, bg="#262626", text="附件管理", fg="#9A9A9A", height=3, cursor="hand2")
#         choice_003.pack(fill="x", side="top")
#
#         def choose_001(evt):
#             choice_001.config(fg="#649AFA")
#             choice_002.config(fg="#9A9A9A")
#             choice_003.config(fg="#9A9A9A")
#             self.change_panel("base_setting")
#
#         def choose_002(evt):
#             choice_001.config(fg="#9A9A9A")
#             choice_002.config(fg="#649AFA")
#             choice_003.config(fg="#9A9A9A")
#             self.change_panel("product_manager")
#
#         def choose_003(evt):
#             choice_001.config(fg="#9A9A9A")
#             choice_002.config(fg="#9A9A9A")
#             choice_003.config(fg="#649AFA")
#             self.change_panel("enclosure_manager")
#
#         choice_001.bind("<Button-1>", choose_001)
#         choice_002.bind("<Button-1>", choose_002)
#         choice_003.bind("<Button-1>", choose_003)
#         choice_001.bind("<Enter>", self.choice_enter)
#         choice_002.bind("<Enter>", self.choice_enter)
#         choice_003.bind("<Enter>", self.choice_enter)
#         choice_001.bind("<Leave>", self.choice_leave)
#         choice_002.bind("<Leave>", self.choice_leave)
#         choice_003.bind("<Leave>", self.choice_leave)
#
#         panel_list = dict()
#         base_setting_frame = tkinter.Frame(self.window, bg="#323232", bd=0, padx=20, pady=20)
#         base_setting_label = tkinter.Label(base_setting_frame, text="无可用设置", font="黑体 25", fg="#646464",
#                                            bg="#323232")
#         base_setting_label.pack()
#         panel_list["base_setting"] = base_setting_frame
#
#         product_manager_frame = tkinter.Frame(self.window, bg="#323232", bd=0, padx=20, pady=20)
#         product_input_frame = tkinter.Frame(product_manager_frame, bg="#464646", bd=0, padx=20, pady=10)
#         product_detail_frame = tkinter.Frame(product_manager_frame, bg="#464646", bd=0, padx=20, pady=20)
#         product_input_frame.place(relwidth=1, height=150)
#         product_detail_frame.place(relwidth=1, y=170, relheight=1, height=-170)
#         product_input_button = tkinter.Label(product_input_frame, bg="#649AFA", fg="#E4E4E4", cursor="hand2",
#                                              text="添加", width=8)
#         product_input_button.bind("<Enter>", self.button_enter)
#         product_input_button.bind("<Leave>", self.button_leave)
#         product_line01 = tkinter.Frame(product_input_frame, bg="#464646")
#         product_name_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="产品名称:")
#
#         # style = tkinter.ttk.Style()
#         # style.configure("TCombobox", fieldbackground="#646464", background="#646464", darkcolor="#323232",
#         #                 foreground="#646464", padding=5, selectbackground="#646464", focusfill="#646464")
#
#         try:
#             combostyle = tkinter.ttk.Style()
#             combostyle.theme_create('combostyle', parent='clam',
#                                     settings={'TCombobox':
#                                                   {'configure':
#                                                        {'selectbackground': '#646464',
#                                                         'fieldbackground': '#646464',
#                                                         'background': '#646464',
#                                                         'foreground': "#A0A0A0",
#                                                         'arrowsize': 15,
#                                                         'lightcolor': "#646464",
#                                                         'arrowcolor': "#A0A0A0",
#                                                         'selectforeground': "#929292",
#                                                         'padding': 6
#                                                         }}}
#                                     )
#             combostyle.theme_use('combostyle')
#
#             style = tkinter.ttk.Style()
#             style.element_create("Custom.Treeheading.border", "from", "default")
#             style.layout("Custom.Treeview.Heading", [
#                 ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
#                 ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
#                     ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
#                         ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
#                         ("Custom.Treeheading.text", {'sticky': 'we'})
#                     ]})
#                 ]}),
#             ])
#             head_font = ('黑体', '12')
#             content_font = ('宋体', '12')
#             style.configure("Custom.Treeview.Heading",
#                             background="#646464", foreground="#E4E4E4", relief="flat", font=head_font)
#             style.configure("Custom.Treeview", background="#323232", foreground="#A0A0A0", fieldbackground="#323232",
#                             highlightthickness=0, font=content_font)
#             style.map("Custom.Treeview.Heading",
#                       relief=[('active', 'groove'), ('pressed', 'sunken')])
#         except BaseException:
#             print("主题已添加")
#
#         combobox_font = ('黑体', '14')
#         self.window.option_add("*TCombobox*Listbox.font", combobox_font)
#         self.window.option_add("*TCombobox*Listbox.background", "#464646")
#         self.window.option_add("*TCombobox*Listbox.foreground", "#E4E4E4")
#         self.window.option_add("*TCombobox*Listbox.selectBackground", "#649AFA")
#
#         product_name_cb = tkinter.ttk.Combobox(product_line01, state="readonly", font=combobox_font, width=15)
#         product_name_cb["value"] = tuple(product_type.keys())
#         product_name_cb.current(0)
#         product_type_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="型号:")
#         product_type_cb = tkinter.ttk.Combobox(product_line01, state="readonly", font=combobox_font, width=8)
#         product_type_cb["value"] = tuple(product_type["框架断路器"])
#         product_type_cb.current(0)
#         product_type_entry = tkinter.Text(product_line01, bg="#646464", fg="#A0A0A0",
#                                           highlightbackground="#A0A0A0",
#                                           highlightcolor="#649AFA", bd=0, highlightthickness=1,
#                                           insertbackground="#A0A0A0",
#                                           height=1, width=12, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
#         product_current_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="电流:")
#         product_current_entry = tkinter.Text(product_line01, bg="#646464", fg="#A0A0A0",
#                                              highlightbackground="#A0A0A0",
#                                              highlightcolor="#649AFA", bd=0, highlightthickness=1,
#                                              insertbackground="#A0A0A0",
#                                              height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
#         product_price_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="面价:")
#         product_price_entry = tkinter.Text(product_line01, bg="#646464", fg="#A0A0A0",
#                                            highlightbackground="#A0A0A0",
#                                            highlightcolor="#649AFA", bd=0, highlightthickness=1,
#                                            insertbackground="#A0A0A0",
#                                            height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
#
#         product_line02 = tkinter.Frame(product_input_frame, bg="#323232", padx=10, pady=5)
#         product_adjunctName_label = tkinter.Label(product_line02, bg="#323232", fg="#A0A0A0", text="附加:")
#         product_adjunctName_entry = tkinter.Text(product_line02, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
#                                                  highlightcolor="#649AFA", bd=0, highlightthickness=1,
#                                                  insertbackground="#A0A0A0",
#                                                  height=1, width=19, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
#         product_adjunctPrice_label = tkinter.Label(product_line02, bg="#323232", fg="#A0A0A0", text="价格:")
#         product_adjunctPrice_entry = tkinter.Text(product_line02, bg="#464646", fg="#A0A0A0",
#                                                   highlightbackground="#A0A0A0",
#                                                   highlightcolor="#649AFA", bd=0, highlightthickness=1,
#                                                   insertbackground="#A0A0A0",
#                                                   height=1, width=16, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
#         product_adjunct_add = tkinter.Label(product_line02, bg="#649AFA", fg="#E4E4E4", text="+", cursor="hand2",
#                                             padx=8, pady=0, font="黑体 20")
#         product_input_button.pack(side="right", fill="y")
#         tkinter.Frame(product_input_frame, width=10, bg="#464646").pack(side="right", fill="y")
#         product_standard_canvas = StandardBar(master=product_line02, bg="#323232")
#         product_standard_canvas.get_canvas().pack(side="bottom", fill="x")
#         tkinter.Frame(product_line02, height=5, bg="#323232").pack(side="bottom", fill="x")
#
#         product_name_label.pack(side="left")
#         product_name_cb.pack(side="left")
#         tkinter.Frame(product_line01, bg="#464646", width=10).pack(side="left")
#         product_type_label.pack(side="left")
#         product_type_cb.pack(side="left")
#         tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="-").pack(side="left")
#         product_type_entry.pack(side="left")
#         tkinter.Frame(product_line01, bg="#464646", width=10).pack(side="left")
#         product_current_label.pack(side="left")
#         product_current_entry.pack(side="left")
#         # tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="A", font="黑体 14", padx=3).pack(side="left")
#         tkinter.Frame(product_line01, bg="#464646", width=10).pack(side="left")
#         product_price_label.pack(side="left")
#         product_price_entry.pack(side="left")
#         tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="元", font="黑体 14", padx=3).pack(side="left")
#         product_line01.pack(side="top", fill="x")
#
#         tkinter.Frame(product_input_frame, bg="#464646", height=10).pack(side="top")
#
#         product_adjunctName_label.pack(side="left")
#         product_adjunctName_entry.pack(side="left")
#         tkinter.Frame(product_line02, bg="#323232", width=10).pack(side="left")
#         product_adjunctPrice_label.pack(side="left")
#         product_adjunctPrice_entry.pack(side="left")
#         tkinter.Frame(product_line02, bg="#323232", width=10).pack(side="left")
#         product_adjunct_add.pack(side="left")
#         product_line02.pack(side="top", fill="x")
#
#         panel_list["product_manager"] = product_manager_frame
#
#         enclosure_manager_frame = tkinter.Frame(self.window, bg="#323232", bd=0, padx=20, pady=20)
#         enclosure_manager_label = tkinter.Label(enclosure_manager_frame, text="该功能已被移除", font="黑体 25", fg="#646464",
#                                                 bg="#323232")
#         enclosure_manager_label.pack()
#         panel_list["enclosure_manager"] = enclosure_manager_frame
#         widget_list = dict()
#         widget_list["product_standard_canvas"] = product_standard_canvas
#         widget_list["product_adjunctName_entry"] = product_adjunctName_entry
#         widget_list["product_adjunctPrice_entry"] = product_adjunctPrice_entry
#         widget_list["product_name_cb"] = product_name_cb
#         widget_list["product_type_cb"] = product_type_cb
#         widget_list["product_type_entry"] = product_type_entry
#         widget_list["product_current_entry"] = product_current_entry
#         widget_list["product_price_entry"] = product_price_entry
#
#         self.data["panel_list"] = panel_list
#         self.data["widget_list"] = widget_list
#
#         self.change_panel("product_manager")
#
#         product_adjunct_add.bind("<Button-1>", self.add_adjunct)
#         product_name_cb.bind("<<ComboboxSelected>>", self.product_name_change)
#
#         # 下面是产品库的布局
#         search_image = tkinter.PhotoImage(file="img/search_icon.png", width=35, height=35)
#         self.data["search_image"] = search_image
#         product_detail_line01 = tkinter.Frame(product_detail_frame, bg="#464646")
#         product_screen_label01 = tkinter.Label(product_detail_line01, bg="#464646", fg="#A0A0A0", text="产品名称:")
#         screen_name_cb = tkinter.ttk.Combobox(product_detail_line01, state="readonly", font=combobox_font, width=15)
#         keys = list(product_type.keys())
#         keys.insert(0, "全部")
#         screen_name_cb["value"] = tuple(keys)
#         screen_name_cb.current(0)
#         product_screen_label02 = tkinter.Label(product_detail_line01, bg="#464646", fg="#A0A0A0", text="型号:")
#         screen_type_cb = tkinter.ttk.Combobox(product_detail_line01, state="readonly", font=combobox_font, width=8)
#         screen_type_cb["value"] = tuple(["全部"])
#         screen_type_cb.current(0)
#         product_search_entry = tkinter.Text(product_detail_line01, bg="#646464", fg="#A0A0A0",
#                                             highlightbackground="#A0A0A0",
#                                             highlightcolor="#649AFA", bd=0, highlightthickness=1,
#                                             insertbackground="#A0A0A0",
#                                             height=1, wrap="none", undo=True, maxundo=-1, padx=10,
#                                             pady=5)
#         product_search_button = tkinter.Label(product_detail_line01, bg="#464646", image=search_image, cursor="hand2")
#         # product_list_box = tkinter.Listbox(product_detail_frame, bg="#323232", bd=0, highlightcolor="#A0A0A0",
#         #                                    highlightbackground="#A0A0A0", font="宋体 14", selectforeground="#E4E4E4",
#         #                                    selectmode="extended", setgrid=False, selectbackground="#649AFA",
#         #                                    fg="#A0A0A0")
#
#         columns = ("name", "type", "adjunct", "price", "adjunctPrice")
#         product_list_box = tkinter.ttk.Treeview(product_detail_frame, show="headings", select="extended",
#                                                 columns=columns, style="Custom.Treeview")
#         product_list_box.heading("name", text="产品名称")
#         product_list_box.heading("type", text="型号及规格")
#         product_list_box.heading("adjunct", text="附加")
#         product_list_box.heading("price", text="面价")
#         product_list_box.heading("adjunctPrice", text="总附加价格")
#         product_list_box.column("name", width=150, anchor="w")
#         product_list_box.column("type", width=150, anchor="w")
#         product_list_box.column("adjunct", width=500, anchor="w")
#         product_list_box.column("price", width=80, anchor="w")
#         product_list_box.column("adjunctPrice", width=80, anchor="w")
#         # test_name = ["智能型万能式断路器", "智能型万能式断路器", "微型断路器", "塑壳断路器", "高压真空断路器"]
#         # test_type = ["RMW1-2000S/3P", "RMW2-2000S/3P", "RMC3-125", "RMM3-630S/3300", "RMVS1-12/630-25"]
#         # test_adjunct = ["RMW1-2000S/3P 1250 抽屉式 bse4 控制电压:AC230V +门框 +相间隔板+配4组转换辅助触头",
#         #                 "RMW1-2000S/4P 1250 抽屉式 bse4 控制电压:AC230V +门框 +相间隔板+配4组转换辅助触头/延时欠电压脱扣器AC230V延时3S+2合1缆绳联锁",
#         #                 "", "分励AC220V", "相距210mm 固定式 合/分闸线圈/储能电机AC220V 闭锁线圈"]
#         # test_price = ["16700", "21700", "330", "210", "16000"]
#         # test_adjunctPrice = ["80", "80", "0", "0", "0"]
#
#         def select(event):
#             selection = product_list_box.selection()
#             for i in product_list_box.get_children():
#                 if i in selection:
#                     product_list_box.tag_configure(i, background="#649AFA", foreground="#E4E4E4")
#                 else:
#                     product_list_box.tag_configure(i, background="#323232", foreground="#A0A0A0")
#
#         product_list_box.bind('<<TreeviewSelect>>', select)
#         self.data["product_treeview"] = product_list_box
#         self.data["product_id_list"] = list()
#         self.products_read()
#         # self.product_list_set(test_name, test_type, test_adjunct, test_price, test_adjunctPrice)
#
#         product_listbox_scroll = tkinter.Scrollbar(product_detail_frame, command=product_list_box.yview)
#         product_list_box.configure(yscrollcommand=product_listbox_scroll.set)
#         product_detail_line02 = tkinter.Frame(product_detail_frame, bg="#464646", pady=10)
#         product_list_delete = tkinter.Label(product_detail_line02, bg="#646464", fg="#A0A0A0", text="删除选中产品",
#                                             cursor="arrow", padx=8, pady=4, font="黑体 14")
#
#         lock_image = tkinter.PhotoImage(file="img/lock_icon.png", width=35, height=35)
#         unlock_image = tkinter.PhotoImage(file="img/unlock_icon.png", width=35, height=35)
#         self.data["lock_image"] = lock_image
#         self.data["unlock_image"] = unlock_image
#         self.data["delete_lock"] = True
#         product_delete_lock = tkinter.Label(product_detail_line02, bg="#464646", image=lock_image, cursor="hand2")
#         # product_list_delete.bind("<Enter>", self.button_enter)
#         # product_list_delete.bind("<Leave>", self.button_leave)
#         product_search_button.pack(side="right")
#         product_screen_label01.pack(side="left")
#         screen_name_cb.pack(side="left")
#         tkinter.Frame(product_detail_line01, bg="#464646", width=10).pack(side="left")
#         product_screen_label02.pack(side="left")
#         screen_type_cb.pack(side="left")
#         tkinter.Frame(product_detail_line01, bg="#464646", width=20).pack(side="left")
#         product_search_entry.pack(side="right", fill="x")
#         product_detail_line01.pack(side="top", fill="x")
#         product_list_delete.pack(side="right")
#         product_delete_lock.pack(side="right")
#         product_detail_line02.pack(side="bottom", fill="x")
#         tkinter.Frame(product_detail_frame, bg="#464646", height=20).pack(side="top")
#         product_listbox_scroll.pack(side="right", fill="y")
#         product_list_box.pack(side="top", fill="both", expand=1)
#
#         widget_list["screen_name_cb"] = screen_name_cb
#         widget_list["screen_type_cb"] = screen_type_cb
#         widget_list["product_list_delete"] = product_list_delete
#         widget_list["product_delete_lock"] = product_delete_lock
#         widget_list["product_search_entry"] = product_search_entry
#
#         screen_name_cb.bind("<<ComboboxSelected>>", self.screen_name_change)
#         product_delete_lock.bind("<Button-1>", self.lock_change)
#         product_input_button.bind("<Button-1>", self.add_product)
#         # product_list_delete.bind("<Button-1>", self.delete_product)
#         # product_adjunctPrice_entry.bind("<Key>", self.number_limit)
#
#         def to_search(evt):
#             self.search()
#             return 'break'
#
#         def return_disabled(evt):
#             return "break"
#
#         for i in widget_list:
#             if type(widget_list[i]) is tkinter.Text:
#                 widget_list[i].bind("<Return>", return_disabled)
#
#         product_search_button.bind("<Button-1>", to_search)
#         product_search_entry.unbind("<Return>")
#         product_search_entry.bind("<Return>", to_search)
#         screen_type_cb.bind("<<ComboboxSelected>>", to_search)
#
#     def product_list_set(self, name_list, type_list, adjunct_list, price_list, adjunctPrice_list, pid_list):
#         self.data["pid_list"] = pid_list
#         # product_id_list = list()
#         for i in range(len(name_list)):
#             id_tag = str(pid_list[i])
#             # product_id_list.append(id_tag)
#             self.data["product_treeview"].insert('', i,
#                                                  values=(name_list[i], type_list[i], adjunct_list[i], price_list[i],
#                                                          adjunctPrice_list[i]), tags=(id_tag, "all"), iid=id_tag)
#         # self.data["product_id_list"] = product_id_list
#
#     def lock_change(self, evt):
#         if self.data["delete_lock"]:
#             self.data["widget_list"]["product_delete_lock"].configure(image=self.data["unlock_image"])
#             self.data["widget_list"]["product_list_delete"].configure(bg="#649AFA", fg="#E4E4E4", cursor="hand2")
#             self.data["widget_list"]["product_list_delete"].bind("<Enter>", self.button_enter)
#             self.data["widget_list"]["product_list_delete"].bind("<Leave>", self.button_leave)
#             self.data["widget_list"]["product_list_delete"].bind("<Button-1>", self.delete_product)
#         else:
#             self.data["widget_list"]["product_delete_lock"].configure(image=self.data["lock_image"])
#             self.data["widget_list"]["product_list_delete"].configure(bg="#646464", fg="#A0A0A0", cursor="arrow")
#             self.data["widget_list"]["product_list_delete"].unbind("<Enter>")
#             self.data["widget_list"]["product_list_delete"].unbind("<Leave>")
#             self.data["widget_list"]["product_list_delete"].unbind("<Button-1>")
#         self.data["delete_lock"] = not self.data["delete_lock"]
#
#     def clear(self):
#         self.data["widget_list"]["product_type_entry"].delete("1.0", "end-1c")
#         self.data["widget_list"]["product_current_entry"].delete("1.0", "end-1c")
#         self.data["widget_list"]["product_price_entry"].delete("1.0", "end-1c")
#         self.data["widget_list"]["product_standard_canvas"].delete_all()
#
#     def category_return(self):
#         self.data["widget_list"]["screen_name_cb"].current(0)
#         self.data["widget_list"]["screen_type_cb"]["value"] = ("全部", )
#         self.data["widget_list"]["screen_type_cb"].current(0)
#         self.data["widget_list"]["product_search_entry"].delete("1.0", "end")
#
#     def delete_product(self, evt):
#         selection = self.data["product_treeview"].selection()
#         data_loader = self.data["data_loader"]
#         for i in selection:
#             data_loader.del_data(int(i))
#         data_loader.save()
#         self.products_read()
#         self.lock_change(None)
#         self.category_return()
#
#     def add_product(self, evt):
#         product_name = self.data["widget_list"]["product_name_cb"].get()
#         product_type = "%s-%s" % (self.data["widget_list"]["product_type_cb"].get(),
#                                   self.data["widget_list"]["product_type_entry"].get("1.0", 'end-1c'))
#         product_current = self.data["widget_list"]["product_current_entry"].get("1.0", 'end-1c')
#         product_price = self.data["widget_list"]["product_price_entry"].get("1.0", 'end-1c')
#         product_adjunct_list = self.data["widget_list"]["product_standard_canvas"].get_items()
#         pattern = r'^([0-9]+(A|(mA)))?$'
#         if not re.match(pattern, product_current):
#             warning_window = WarningWindow(self.window, "电流格式错误，电流应留空，或以mA或A为单位")
#             return
#         pattern = r'[0-9]+(.[0-9]+)?'
#         if not re.match(pattern, product_price):
#             warning_window = WarningWindow(self.window, "价格填写错误，应为数字，不能留空")
#             return
#         product_price = float(product_price)
#         data_loader = self.data["data_loader"]
#         new_product = Product(unit="台", raw_price=product_price, adjunct=product_adjunct_list, current=product_current,
#                               model=product_type, name=product_name)
#         data_loader.add_data(new_product)
#         data_loader.save()
#         self.products_read()
#         self.category_return()
#
#     def product_load(self, product_list):
#         for i in self.data["product_treeview"].get_children():
#             self.data["product_treeview"].delete(i)
#         name_list = list()
#         type_list = list()
#         price_list = list()
#         adjunct_list = list()
#         adjunctPrice_list = list()
#         pid_list = list()
#         for i in product_list:
#             pid_list.append(i[0])
#             product = i[1]
#             name_list.append(product.get_name())
#             type_list.append(product.get_model())
#             price_list.append(product.get_raw_price())
#             adjunct_list.append(product.get_adjunct())
#             adjunctPrice_list.append(product.get_adjunct_price())
#         self.product_list_set(name_list, type_list, adjunct_list, price_list, adjunctPrice_list, pid_list)
#
#     def products_read(self):
#         data_loader = self.data["data_loader"]
#         self.product_load(data_loader.get_products_list())
#
#     @staticmethod
#     def get_str_length(string):
#         str_length = 0
#         for i in string:
#             if u'\u4e00' <= i <= u'\u9fa5':
#                 str_length += 2
#             else:
#                 str_length += 1
#         return str_length
#
#     @staticmethod
#     def string_cut(string, length):
#         now_length = 0
#         now_string = ""
#         for i in string:
#             if u'\u4e00' <= i <= u'\u9fa5':
#                 now_string += i
#                 now_length += 2
#             else:
#                 now_string += i
#                 now_length += 1
#             if now_length > length - 2:
#                 now_string = now_string[0:-1] + "…"
#                 return now_string
#         return string
#
#     @staticmethod
#     def string_format(string, length, fill=" "):
#         str_length = SettingWindow.get_str_length(string)
#         if str_length > length:
#             string = SettingWindow.string_cut(string, length)
#             str_length = SettingWindow.get_str_length(string)
#         length_diff = length - str_length
#         while length_diff > 0:
#             string += fill
#             length_diff -= 1
#         return string
#
#     @staticmethod
#     def items_format(name_list, type_list, adjunct_list, price_list, adjunctPrice_list):
#         form_list = list()
#         for i in range(len(name_list)):
#             form_name = SettingWindow.string_format(name_list[i], 20)
#             form_type = SettingWindow.string_format(type_list[i], 18)
#             form_adjunct = SettingWindow.string_format(adjunct_list[i], 40)
#             form_price = SettingWindow.string_format(price_list[i], 8)
#             form_adjunctPrice = SettingWindow.string_format(adjunctPrice_list[i], 8)
#             form_list.append(" %s %s %s %s %s" % (form_name, form_type, form_adjunct, form_price, form_adjunctPrice))
#         return form_list
#
#     def search(self):
#         name = self.data["widget_list"]["screen_name_cb"].get()
#         type = self.data["widget_list"]["screen_type_cb"].get()
#         name = None if name == "全部" else name
#         type = None if type == "全部" else type
#         keyword = self.data["widget_list"]["product_search_entry"].get("1.0", 'end-1c')
#         data_loader = self.data["data_loader"]
#         product_list = DataLoader.search(data_loader.get_products_list(), name, type, keyword)
#         self.product_load(product_list)
#
#     def screen_name_change(self, evt):
#         choice = self.data["widget_list"]["screen_name_cb"].get()
#         keys = list(product_type[choice]) if choice != "全部" else list()
#         keys.insert(0, "全部")
#         self.data["widget_list"]["screen_type_cb"]["value"] = keys
#         self.data["widget_list"]["screen_type_cb"].current(0)
#         self.search()
#
#     def product_name_change(self, evt):
#         choice = self.data["widget_list"]["product_name_cb"].get()
#         self.data["widget_list"]["product_type_cb"]["value"] = tuple(product_type[choice])
#         self.data["widget_list"]["product_type_cb"].current(0)
#
#     def add_adjunct(self, evt):
#         name = self.data["widget_list"]["product_adjunctName_entry"].get("1.0", 'end-1c')
#         name = name.replace("\n", "")
#         price = self.data["widget_list"]["product_adjunctPrice_entry"].get("1.0", 'end-1c')
#         pattern = r'[0-9]+(.[0-9]+)?'
#         if not re.match(pattern, price) and price != "":
#             warning_window = WarningWindow(self.window, "价格必须为数字或空")
#             return
#         price = float(price) if price != "" else 0.0
#         if name != "" and self.data["widget_list"]["product_standard_canvas"].add_item(name, price):
#             self.data["widget_list"]["product_adjunctName_entry"].delete("0.0", "end")
#             self.data["widget_list"]["product_adjunctPrice_entry"].delete("0.0", "end")
#
#     def number_limit(self, evt):
#         target = evt.widget
#         text = target.get("1.0", "end")
#         target_text = ""
#         for i in text:
#             if i in "123456789.":
#                 target_text += i
#         if target_text != text:
#             target.delete("1.0", "end")
#             target.insert("1.0", target_text)
#
#     @staticmethod
#     def button_enter(evt):
#         evt.widget.config(bg="#84AAFF")
#
#     @staticmethod
#     def button_leave(evt):
#         evt.widget.config(bg="#649AFA")
#
#     @staticmethod
#     def choice_enter(evt):
#         evt.widget.config(bg="#3A3A3A")
#
#     @staticmethod
#     def choice_leave(evt):
#         evt.widget.config(bg="#262626")
#
#     def change_panel(self, panel):
#         for i in self.data["panel_list"]:
#             self.data["panel_list"][i].place_forget()
#         self.data["panel_list"][panel].place(x=160, relwidth=1, width=-160, relheight=1)


