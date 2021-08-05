import tkinter
import tkinter.ttk
import re
from gui.child_window import ChildWindow
from gui.warning_window import WarningWindow
from gui.assembly import StandardBar
from utils.dataLoader import DataLoader
from utils.exception import *
from utils.product import Product
from pathlib import Path

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


class SettingWindow(ChildWindow):
    setting_count = 0
    settings = None
    settings_modify = None

    @staticmethod
    def check():
        return __class__.setting_count < 1

    def close(self):
        __class__.setting_count -= 1
        logging_level = str(self.data["logging_level"].get())
        quote_contact = self.data["quote_contact_entry"].get("1.0", "end-1c")
        quote_tel = self.data["quote_tel_entry"].get("1.0", "end-1c")
        quote_qq = self.data["quote_qq_entry"].get("1.0", "end-1c")

        if logging_level != __class__.settings["logging_level"]:
            __class__.settings["logging_level"] = logging_level
            __class__.settings_modify = True
        if logging_level != __class__.settings["quote_contact"]:
            __class__.settings["quote_contact"] = quote_contact
            __class__.settings_modify = True
        if logging_level != __class__.settings["quote_tel"]:
            __class__.settings["quote_tel"] = quote_tel
            __class__.settings_modify = True
        if logging_level != __class__.settings["quote_qq"]:
            __class__.settings["quote_qq"] = quote_qq
            __class__.settings_modify = True

        if __class__.settings_modify:
            __class__.settings_modify = False
            setting_path = Path('setting.yaml')
            with setting_path.open('w', encoding='utf8') as f:
                f.write('\n'.join([f'{i}:{v}'for i, v in __class__.settings.items()]))
        if self.data.get("command") is not None:
            self.data["command"]()
        self.data["data_loader"].save()
        super().close()

    @classmethod
    def load_setting(cls):
        setting_path = Path('setting.yaml')
        if not cls.settings:
            cls.settings_modify = False
            cls.settings = {}
            if setting_path.exists():
                with setting_path.open('r', encoding='utf8') as f:
                    for line in f.readlines():
                        setting = line.strip().split(':')
                        cls.settings[setting[0]] = setting[1]
        if 'logging_level' not in __class__.settings:
            cls.settings["logging_level"] = '2'

        if 'quote_contact' not in __class__.settings:
            cls.settings["quote_contact"] = ""

        if 'quote_tel' not in __class__.settings:
            cls.settings["quote_tel"] = ""

        if 'quote_qq' not in __class__.settings:
            cls.settings["quote_qq"] = ""

    def gui_init(self, window):
        self.load_setting()
        logging_level = tkinter.IntVar()
        logging_level.set(__class__.settings["logging_level"])
        self.data["logging_level"] = logging_level

        __class__.setting_count += 1
        self.data["data_loader"].refresh()
        menu_frame = tkinter.Frame(self.window, bg="#262626", bd=0)
        menu_frame.place(width=160, relheight=1)

        choice_001 = tkinter.Label(menu_frame, bg="#262626", text="基础设置", fg="#9A9A9A", height=3, cursor="hand2")
        choice_001.pack(fill="x", side="top")
        choice_002 = tkinter.Label(menu_frame, bg="#262626", text="产品管理", fg="#649AFA", height=3, cursor="hand2")
        choice_002.pack(fill="x", side="top")
        choice_003 = tkinter.Label(menu_frame, bg="#262626", text="附件管理", fg="#9A9A9A", height=3, cursor="hand2")
        choice_003.pack(fill="x", side="top")

        def choose_001(evt):
            choice_001.config(fg="#649AFA")
            choice_002.config(fg="#9A9A9A")
            choice_003.config(fg="#9A9A9A")
            self.change_panel("base_setting")

        def choose_002(evt):
            choice_001.config(fg="#9A9A9A")
            choice_002.config(fg="#649AFA")
            choice_003.config(fg="#9A9A9A")
            self.change_panel("product_manager")

        def choose_003(evt):
            choice_001.config(fg="#9A9A9A")
            choice_002.config(fg="#9A9A9A")
            choice_003.config(fg="#649AFA")
            self.change_panel("enclosure_manager")

        choice_001.bind("<Button-1>", choose_001)
        choice_002.bind("<Button-1>", choose_002)
        choice_003.bind("<Button-1>", choose_003)
        choice_001.bind("<Enter>", self.choice_enter)
        choice_002.bind("<Enter>", self.choice_enter)
        choice_003.bind("<Enter>", self.choice_enter)
        choice_001.bind("<Leave>", self.choice_leave)
        choice_002.bind("<Leave>", self.choice_leave)
        choice_003.bind("<Leave>", self.choice_leave)

        panel_list = dict()
        base_setting_frame = tkinter.Frame(self.window, bg="#323232", bd=0, padx=20, pady=20)
        base_line01 = tkinter.Frame(base_setting_frame, bg="#464646", padx=20, pady=10)
        base_line01_01 = tkinter.Frame(base_line01, bg="#464646")
        tkinter.Label(base_line01_01, bg="#464646", fg="#649AFA", text="报价单默认值", font="黑体 18").pack(side="left")
        base_line01_01.grid(column=0, row=0, rowspan=1, pady=5, padx=5, sticky=tkinter.W)
        quote_contact_label = tkinter.Label(base_line01, text="报价联系人:", fg="#A0A0A0", bg="#464646")
        quote_tel_label = tkinter.Label(base_line01, text="电话/传真:", fg="#A0A0A0", bg="#464646")
        quote_qq_label = tkinter.Label(base_line01, text="联系qq:", fg="#A0A0A0", bg="#464646")
        quote_contact_entry = tkinter.Text(base_line01, bg="#363636", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                           highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                           insertbackground="#A0A0A0",
                                           height=1, width=10, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        quote_tel_entry = tkinter.Text(base_line01, bg="#363636", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                       highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                       insertbackground="#A0A0A0",
                                       height=1, width=25, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        quote_qq_entry = tkinter.Text(base_line01, bg="#363636", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                      highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                      insertbackground="#A0A0A0",
                                      height=1, width=25, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        quote_contact_label.grid(column=0, row=1, pady=5, padx=5, sticky=tkinter.W)
        quote_contact_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tkinter.W)
        quote_tel_label.grid(column=0, row=2, pady=5, padx=5, sticky=tkinter.W)
        quote_tel_entry.grid(column=1, row=2, pady=5, padx=5, sticky=tkinter.W)
        quote_qq_label.grid(column=0, row=3, pady=5, padx=5, sticky=tkinter.W)
        quote_qq_entry.grid(column=1, row=3, pady=5, padx=5, sticky=tkinter.W)
        base_line01.pack(side="top", fill="x")
        tkinter.Frame(base_setting_frame, bg="#323232", height=15).pack(side="top")

        def return_break(evt):
            return "break"

        quote_contact_entry.bind("<Return>", return_break)
        quote_tel_entry.bind("<Return>", return_break)
        quote_qq_entry.bind("<Return>", return_break)

        quote_contact_entry.insert("1.0", __class__.settings["quote_contact"])
        quote_tel_entry.insert("1.0", __class__.settings["quote_tel"])
        quote_qq_entry.insert("1.0", __class__.settings["quote_qq"])

        self.data["quote_contact_entry"] = quote_contact_entry
        self.data["quote_tel_entry"] = quote_tel_entry
        self.data["quote_qq_entry"] = quote_qq_entry

        base_line02 = tkinter.Frame(base_setting_frame, bg="#464646", padx=20, pady=10)
        logging_level_label = tkinter.Label(base_line02, text="日志等级:", fg="#A0A0A0", bg="#464646")
        base_line02.pack(side="top", fill="x")
        logging_level_label.pack(side="left")
        self.data["logging_level_rb"] = list()
        choice_list = [("Debug", 0), ("Info", 1), ("Warning", 2), ("Error", 3), ("Fatal", 4)]

        def get_choose_function(index):
            def function(evt):
                widget = evt.widget
                for item in self.data["logging_level_rb"]:
                    item.config(fg="#7A7A7A", font="黑体 16")
                widget.config(fg="#649AFA", font="黑体 18")
                self.data["logging_level"].set(int(index))
            return function

        for i in choice_list:
            # choice = tkinter.Radiobutton(base_line02, text=i[0], value=i[1], variable=logging_level, bg="#464646",
            #                              fg="#9A9A9A", selectcolor="#262626", activebackground="#464646",
            #                              activeforeground="#9A9A9A")
            # choice.pack(side="left")
            # self.data["logging_level_rb"].append(choice)
            if i[1] == self.data["logging_level"].get():
                choice = tkinter.Label(base_line02, text=i[0], bg="#464646", fg="#649AFA", font="黑体 18", padx=20, cursor="hand2")
            else:
                choice = tkinter.Label(base_line02, text=i[0], bg="#464646", fg="#7A7A7A", font="黑体 16", padx=20, cursor="hand2")
            choice.bind("<Button-1>", get_choose_function(i[1]))
            choice.pack(side="left")
            self.data["logging_level_rb"].append(choice)
        panel_list["base_setting"] = base_setting_frame

        product_manager_frame = tkinter.Frame(self.window, bg="#323232", bd=0, padx=20, pady=20)
        product_input_frame = tkinter.Frame(product_manager_frame, bg="#464646", bd=0, padx=20, pady=10)
        product_detail_frame = tkinter.Frame(product_manager_frame, bg="#464646", bd=0, padx=20, pady=20)
        product_input_frame.place(relwidth=1, height=150)
        product_detail_frame.place(relwidth=1, y=170, relheight=1, height=-170)
        product_input_button = tkinter.Label(product_input_frame, bg="#649AFA", fg="#E4E4E4", cursor="hand2",
                                             text="添加", width=8)
        product_input_button.bind("<Enter>", self.button_enter)
        product_input_button.bind("<Leave>", self.button_leave)
        product_line01 = tkinter.Frame(product_input_frame, bg="#464646")
        product_name_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="产品名称:")

        # style = tkinter.ttk.Style()
        # style.configure("TCombobox", fieldbackground="#646464", background="#646464", darkcolor="#323232",
        #                 foreground="#646464", padding=5, selectbackground="#646464", focusfill="#646464")

        combobox_font = ('黑体', '14')
        self.window.option_add("*TCombobox*Listbox.font", combobox_font)
        self.window.option_add("*TCombobox*Listbox.background", "#464646")
        self.window.option_add("*TCombobox*Listbox.foreground", "#E4E4E4")
        self.window.option_add("*TCombobox*Listbox.selectBackground", "#649AFA")

        product_name_cb = tkinter.ttk.Combobox(product_line01, state="readonly", font=combobox_font, width=15)
        product_name_cb["value"] = tuple(product_type.keys())
        product_name_cb.current(0)
        product_type_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="型号:")
        product_type_cb = tkinter.ttk.Combobox(product_line01, state="readonly", font=combobox_font, width=8)
        product_type_cb["value"] = tuple(product_type["框架断路器"])
        product_type_cb.current(0)
        product_type_entry = tkinter.Text(product_line01, bg="#646464", fg="#A0A0A0",
                                          highlightbackground="#A0A0A0",
                                          highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                          insertbackground="#A0A0A0",
                                          height=1, width=12, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        product_current_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="电流:")
        product_current_entry = tkinter.Text(product_line01, bg="#646464", fg="#A0A0A0",
                                             highlightbackground="#A0A0A0",
                                             highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                             insertbackground="#A0A0A0",
                                             height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        product_price_label = tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="面价:")
        product_price_entry = tkinter.Text(product_line01, bg="#646464", fg="#A0A0A0",
                                           highlightbackground="#A0A0A0",
                                           highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                           insertbackground="#A0A0A0",
                                           height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)

        product_line02 = tkinter.Frame(product_input_frame, bg="#323232", padx=10, pady=5)
        product_adjunctName_label = tkinter.Label(product_line02, bg="#323232", fg="#A0A0A0", text="附加:")
        product_adjunctName_entry = tkinter.Text(product_line02, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                                 highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                                 insertbackground="#A0A0A0",
                                                 height=1, width=19, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        product_adjunctPrice_label = tkinter.Label(product_line02, bg="#323232", fg="#A0A0A0", text="价格:")
        product_adjunctPrice_entry = tkinter.Text(product_line02, bg="#464646", fg="#A0A0A0",
                                                  highlightbackground="#A0A0A0",
                                                  highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                                  insertbackground="#A0A0A0",
                                                  height=1, width=16, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        product_adjunct_add = tkinter.Label(product_line02, bg="#649AFA", fg="#E4E4E4", text="+", cursor="hand2",
                                            padx=8, pady=0, font="黑体 20")
        product_input_button.pack(side="right", fill="y")
        tkinter.Frame(product_input_frame, width=10, bg="#464646").pack(side="right", fill="y")
        product_standard_canvas = StandardBar(master=product_line02, bg="#323232")
        product_standard_canvas.get_canvas().pack(side="bottom", fill="x")
        tkinter.Frame(product_line02, height=5, bg="#323232").pack(side="bottom", fill="x")

        product_name_label.pack(side="left")
        product_name_cb.pack(side="left")
        tkinter.Frame(product_line01, bg="#464646", width=10).pack(side="left")
        product_type_label.pack(side="left")
        product_type_cb.pack(side="left")
        tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="-").pack(side="left")
        product_type_entry.pack(side="left")
        tkinter.Frame(product_line01, bg="#464646", width=10).pack(side="left")
        product_current_label.pack(side="left")
        product_current_entry.pack(side="left")
        # tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="A", font="黑体 14", padx=3).pack(side="left")
        tkinter.Frame(product_line01, bg="#464646", width=10).pack(side="left")
        product_price_label.pack(side="left")
        product_price_entry.pack(side="left")
        tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="元", font="黑体 14", padx=3).pack(side="left")
        product_line01.pack(side="top", fill="x")

        tkinter.Frame(product_input_frame, bg="#464646", height=10).pack(side="top")

        product_adjunctName_label.pack(side="left")
        product_adjunctName_entry.pack(side="left")
        tkinter.Frame(product_line02, bg="#323232", width=10).pack(side="left")
        product_adjunctPrice_label.pack(side="left")
        product_adjunctPrice_entry.pack(side="left")
        tkinter.Frame(product_line02, bg="#323232", width=10).pack(side="left")
        product_adjunct_add.pack(side="left")
        product_line02.pack(side="top", fill="x")

        panel_list["product_manager"] = product_manager_frame

        enclosure_manager_frame = tkinter.Frame(self.window, bg="#323232", bd=0, padx=20, pady=20)
        enclosure_manager_label = tkinter.Label(enclosure_manager_frame, text="该功能已被移除", font="黑体 25", fg="#646464",
                                                bg="#323232")
        enclosure_manager_label.pack()
        panel_list["enclosure_manager"] = enclosure_manager_frame
        widget_list = dict()
        widget_list["product_standard_canvas"] = product_standard_canvas
        widget_list["product_adjunctName_entry"] = product_adjunctName_entry
        widget_list["product_adjunctPrice_entry"] = product_adjunctPrice_entry
        widget_list["product_name_cb"] = product_name_cb
        widget_list["product_type_cb"] = product_type_cb
        widget_list["product_type_entry"] = product_type_entry
        widget_list["product_current_entry"] = product_current_entry
        widget_list["product_price_entry"] = product_price_entry

        self.data["panel_list"] = panel_list
        self.data["widget_list"] = widget_list

        self.change_panel("product_manager")

        product_adjunct_add.bind("<Button-1>", self.add_adjunct)
        product_name_cb.bind("<<ComboboxSelected>>", self.product_name_change)

        # 下面是产品库的布局
        search_image = tkinter.PhotoImage(file="img/search_icon.png", width=35, height=35)
        self.data["search_image"] = search_image
        product_detail_line01 = tkinter.Frame(product_detail_frame, bg="#464646")
        product_screen_label01 = tkinter.Label(product_detail_line01, bg="#464646", fg="#A0A0A0", text="产品名称:")
        screen_name_cb = tkinter.ttk.Combobox(product_detail_line01, state="readonly", font=combobox_font, width=15)
        keys = list(product_type.keys())
        keys.insert(0, "全部")
        screen_name_cb["value"] = tuple(keys)
        screen_name_cb.current(0)
        product_screen_label02 = tkinter.Label(product_detail_line01, bg="#464646", fg="#A0A0A0", text="型号:")
        screen_type_cb = tkinter.ttk.Combobox(product_detail_line01, state="readonly", font=combobox_font, width=8)
        screen_type_cb["value"] = tuple(["全部"])
        screen_type_cb.current(0)
        product_search_entry = tkinter.Text(product_detail_line01, bg="#646464", fg="#A0A0A0",
                                            highlightbackground="#A0A0A0",
                                            highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                            insertbackground="#A0A0A0",
                                            height=1, wrap="none", undo=True, maxundo=-1, padx=10,
                                            pady=5)
        product_search_button = tkinter.Label(product_detail_line01, bg="#464646", image=search_image, cursor="hand2")
        # product_list_box = tkinter.Listbox(product_detail_frame, bg="#323232", bd=0, highlightcolor="#A0A0A0",
        #                                    highlightbackground="#A0A0A0", font="宋体 14", selectforeground="#E4E4E4",
        #                                    selectmode="extended", setgrid=False, selectbackground="#649AFA",
        #                                    fg="#A0A0A0")

        columns = ("name", "type", "adjunct", "price", "adjunctPrice")
        product_list_box = tkinter.ttk.Treeview(product_detail_frame, show="headings", select="extended",
                                                columns=columns, style="Custom.Treeview")
        product_list_box.heading("name", text="产品名称")
        product_list_box.heading("type", text="型号及规格")
        product_list_box.heading("adjunct", text="附加")
        product_list_box.heading("price", text="面价")
        product_list_box.heading("adjunctPrice", text="总附加价格")
        product_list_box.column("name", width=150, anchor="w")
        product_list_box.column("type", width=150, anchor="w")
        product_list_box.column("adjunct", width=500, anchor="w")
        product_list_box.column("price", width=80, anchor="w")
        product_list_box.column("adjunctPrice", width=80, anchor="w")
        # test_name = ["智能型万能式断路器", "智能型万能式断路器", "微型断路器", "塑壳断路器", "高压真空断路器"]
        # test_type = ["RMW1-2000S/3P", "RMW2-2000S/3P", "RMC3-125", "RMM3-630S/3300", "RMVS1-12/630-25"]
        # test_adjunct = ["RMW1-2000S/3P 1250 抽屉式 bse4 控制电压:AC230V +门框 +相间隔板+配4组转换辅助触头",
        #                 "RMW1-2000S/4P 1250 抽屉式 bse4 控制电压:AC230V +门框 +相间隔板+配4组转换辅助触头/延时欠电压脱扣器AC230V延时3S+2合1缆绳联锁",
        #                 "", "分励AC220V", "相距210mm 固定式 合/分闸线圈/储能电机AC220V 闭锁线圈"]
        # test_price = ["16700", "21700", "330", "210", "16000"]
        # test_adjunctPrice = ["80", "80", "0", "0", "0"]

        def select(event):
            selection = product_list_box.selection()
            for i in product_list_box.get_children():
                if i in selection:
                    product_list_box.tag_configure(i, background="#649AFA", foreground="#E4E4E4")
                else:
                    product_list_box.tag_configure(i, background="#323232", foreground="#A0A0A0")

        product_list_box.bind('<<TreeviewSelect>>', select)
        self.data["product_treeview"] = product_list_box
        self.data["product_id_list"] = list()
        self.products_read()
        # self.product_list_set(test_name, test_type, test_adjunct, test_price, test_adjunctPrice)

        product_listbox_scroll = tkinter.Scrollbar(product_detail_frame, command=product_list_box.yview)
        product_list_box.configure(yscrollcommand=product_listbox_scroll.set)
        product_detail_line02 = tkinter.Frame(product_detail_frame, bg="#464646", pady=10)
        product_list_delete = tkinter.Label(product_detail_line02, bg="#646464", fg="#A0A0A0", text="删除选中产品",
                                            cursor="arrow", padx=8, pady=4, font="黑体 14")

        lock_image = tkinter.PhotoImage(file="img/lock_icon.png", width=35, height=35)
        unlock_image = tkinter.PhotoImage(file="img/unlock_icon.png", width=35, height=35)
        self.data["lock_image"] = lock_image
        self.data["unlock_image"] = unlock_image
        self.data["delete_lock"] = True
        product_delete_lock = tkinter.Label(product_detail_line02, bg="#464646", image=lock_image, cursor="hand2")

        refresh_img = tkinter.PhotoImage(file="img/refresh_icon.png", width=35, height=35)
        refresh_button = tkinter.Label(product_detail_line02, image=refresh_img, bg="#464646", cursor="hand2")
        self.data["refresh_img"] = refresh_img

        def refresh_products(evt):
            self.data["data_loader"].refresh()
            self.search()

        refresh_button.bind("<Button-1>", refresh_products)

        # product_list_delete.bind("<Enter>", self.button_enter)
        # product_list_delete.bind("<Leave>", self.button_leave)
        product_search_button.pack(side="right")
        product_screen_label01.pack(side="left")
        screen_name_cb.pack(side="left")
        tkinter.Frame(product_detail_line01, bg="#464646", width=10).pack(side="left")
        product_screen_label02.pack(side="left")
        screen_type_cb.pack(side="left")
        tkinter.Frame(product_detail_line01, bg="#464646", width=20).pack(side="left")
        product_search_entry.pack(side="right", fill="x")
        product_detail_line01.pack(side="top", fill="x")
        product_list_delete.pack(side="right")
        product_delete_lock.pack(side="right")
        refresh_button.pack(side="left")
        product_detail_line02.pack(side="bottom", fill="x")
        tkinter.Frame(product_detail_frame, bg="#464646", height=20).pack(side="top")
        product_listbox_scroll.pack(side="right", fill="y")
        product_list_box.pack(side="top", fill="both", expand=1)

        widget_list["screen_name_cb"] = screen_name_cb
        widget_list["screen_type_cb"] = screen_type_cb
        widget_list["product_list_delete"] = product_list_delete
        widget_list["product_delete_lock"] = product_delete_lock
        widget_list["product_search_entry"] = product_search_entry

        screen_name_cb.bind("<<ComboboxSelected>>", self.screen_name_change)
        product_delete_lock.bind("<Button-1>", self.lock_change)
        product_input_button.bind("<Button-1>", self.add_product)
        # product_list_delete.bind("<Button-1>", self.delete_product)
        # product_adjunctPrice_entry.bind("<Key>", self.number_limit)

        def to_search(evt):
            self.search()
            return 'break'

        def return_disabled(evt):
            return "break"

        for i in widget_list:
            if type(widget_list[i]) is tkinter.Text:
                widget_list[i].bind("<Return>", return_disabled)

        product_search_button.bind("<Button-1>", to_search)
        product_search_entry.unbind("<Return>")
        product_search_entry.bind("<Return>", to_search)
        screen_type_cb.bind("<<ComboboxSelected>>", to_search)

    def product_list_set(self, name_list, type_list, adjunct_list, price_list, adjunctPrice_list, pid_list):
        self.data["pid_list"] = pid_list
        # product_id_list = list()
        for i in range(len(name_list)):
            id_tag = str(pid_list[i])
            # product_id_list.append(id_tag)
            self.data["product_treeview"].insert('', i,
                                                 values=(name_list[i], type_list[i], adjunct_list[i], price_list[i],
                                                         adjunctPrice_list[i]), tags=(id_tag, "all"), iid=id_tag)
        # self.data["product_id_list"] = product_id_list

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

    def clear(self):
        self.data["widget_list"]["product_type_entry"].delete("1.0", "end-1c")
        self.data["widget_list"]["product_current_entry"].delete("1.0", "end-1c")
        self.data["widget_list"]["product_price_entry"].delete("1.0", "end-1c")
        self.data["widget_list"]["product_standard_canvas"].delete_all()

    def category_return(self):
        self.data["widget_list"]["screen_name_cb"].current(0)
        self.data["widget_list"]["screen_type_cb"]["value"] = ("全部", )
        self.data["widget_list"]["screen_type_cb"].current(0)
        self.data["widget_list"]["product_search_entry"].delete("1.0", "end")

    def delete_product(self, evt):
        selection = self.data["product_treeview"].selection()
        data_loader = self.data["data_loader"]
        for i in selection:
            data_loader.del_data(int(i))
        self.products_read()
        self.lock_change(None)
        self.category_return()

    def add_product(self, evt):
        product_name = self.data["widget_list"]["product_name_cb"].get()
        product_type = "%s-%s" % (self.data["widget_list"]["product_type_cb"].get(),
                                  self.data["widget_list"]["product_type_entry"].get("1.0", 'end-1c'))
        product_current = self.data["widget_list"]["product_current_entry"].get("1.0", 'end-1c')
        product_price = self.data["widget_list"]["product_price_entry"].get("1.0", 'end-1c')
        product_adjunct_list = self.data["widget_list"]["product_standard_canvas"].get_items()
        pattern = r'^([0-9]+(A|(mA)))?$'
        if not re.match(pattern, product_current):
            warning_window = WarningWindow(self.window, "电流格式错误，电流应留空，或以mA或A为单位")
            return
        pattern = r'[0-9]+(.[0-9]+)?'
        if not re.match(pattern, product_price):
            warning_window = WarningWindow(self.window, "价格填写错误，应为数字，不能留空")
            return
        product_price = float(product_price)
        data_loader = self.data["data_loader"]
        new_product = Product(unit="台", raw_price=product_price, adjunct=product_adjunct_list, current=product_current,
                              model=product_type, name=product_name)
        try:
            data_loader.add_data(new_product)
        except ProductAlreadyExist:
            warning_window = WarningWindow(self.window, "产品已存在。")
            return
        self.search()
        self.data["widget_list"]["product_type_entry"].delete("1.0", 'end')
        self.data["widget_list"]["product_current_entry"].delete("1.0", 'end')
        self.data["widget_list"]["product_price_entry"].delete("1.0", 'end')
        self.data["widget_list"]["product_standard_canvas"].delete_all()

    def product_load(self, product_list):
        for i in self.data["product_treeview"].get_children():
            self.data["product_treeview"].delete(i)
        name_list = list()
        type_list = list()
        price_list = list()
        adjunct_list = list()
        adjunctPrice_list = list()
        pid_list = list()
        for i in product_list:
            pid_list.append(i[0])
            product = i[1]
            name_list.append(product.get_name())
            type_list.append(product.get_model())
            price_list.append(product.get_raw_price())
            adjunct_list.append(product.get_adjunct())
            adjunctPrice_list.append(product.get_adjunct_price())
        self.product_list_set(name_list, type_list, adjunct_list, price_list, adjunctPrice_list, pid_list)

    def products_read(self):
        data_loader = self.data["data_loader"]
        self.product_load(data_loader.get_products_list())

    @staticmethod
    def get_str_length(string):
        str_length = 0
        for i in string:
            if u'\u4e00' <= i <= u'\u9fa5':
                str_length += 2
            else:
                str_length += 1
        return str_length

    @staticmethod
    def string_cut(string, length):
        now_length = 0
        now_string = ""
        for i in string:
            if u'\u4e00' <= i <= u'\u9fa5':
                now_string += i
                now_length += 2
            else:
                now_string += i
                now_length += 1
            if now_length > length - 2:
                now_string = now_string[0:-1] + "…"
                return now_string
        return string

    @staticmethod
    def string_format(string, length, fill=" "):
        str_length = SettingWindow.get_str_length(string)
        if str_length > length:
            string = SettingWindow.string_cut(string, length)
            str_length = SettingWindow.get_str_length(string)
        length_diff = length - str_length
        while length_diff > 0:
            string += fill
            length_diff -= 1
        return string

    @staticmethod
    def items_format(name_list, type_list, adjunct_list, price_list, adjunctPrice_list):
        form_list = list()
        for i in range(len(name_list)):
            form_name = SettingWindow.string_format(name_list[i], 20)
            form_type = SettingWindow.string_format(type_list[i], 18)
            form_adjunct = SettingWindow.string_format(adjunct_list[i], 40)
            form_price = SettingWindow.string_format(price_list[i], 8)
            form_adjunctPrice = SettingWindow.string_format(adjunctPrice_list[i], 8)
            form_list.append(" %s %s %s %s %s" % (form_name, form_type, form_adjunct, form_price, form_adjunctPrice))
        return form_list

    def search(self):
        name = self.data["widget_list"]["screen_name_cb"].get()
        type = self.data["widget_list"]["screen_type_cb"].get()
        name = None if name == "全部" else name
        type = None if type == "全部" else type
        keyword = self.data["widget_list"]["product_search_entry"].get("1.0", 'end-1c')
        data_loader = self.data["data_loader"]
        product_list = DataLoader.search(data_loader.get_products_list(), name, type, keyword)
        self.product_load(product_list)

    def screen_name_change(self, evt):
        choice = self.data["widget_list"]["screen_name_cb"].get()
        keys = list(product_type[choice]) if choice != "全部" else list()
        keys.insert(0, "全部")
        self.data["widget_list"]["screen_type_cb"]["value"] = keys
        self.data["widget_list"]["screen_type_cb"].current(0)
        self.search()

    def product_name_change(self, evt):
        choice = self.data["widget_list"]["product_name_cb"].get()
        self.data["widget_list"]["product_type_cb"]["value"] = tuple(product_type[choice])
        self.data["widget_list"]["product_type_cb"].current(0)

    def add_adjunct(self, evt):
        name = self.data["widget_list"]["product_adjunctName_entry"].get("1.0", 'end-1c')
        name = name.replace("\n", "")
        price = self.data["widget_list"]["product_adjunctPrice_entry"].get("1.0", 'end-1c')
        if not re.match(r'^([0-9]+(.[0-9]+)?)?$', price):
            warning_window = WarningWindow(self.window, "价格必须为数字或空")
            return
        price = float(price) if price != "" else 0.0
        if name != "" and self.data["widget_list"]["product_standard_canvas"].add_item(name, price):
            self.data["widget_list"]["product_adjunctName_entry"].delete("0.0", "end")
            self.data["widget_list"]["product_adjunctPrice_entry"].delete("0.0", "end")

    def number_limit(self, evt):
        target = evt.widget
        text = target.get("1.0", "end")
        target_text = ""
        for i in text:
            if i in "123456789.":
                target_text += i
        if target_text != text:
            target.delete("1.0", "end")
            target.insert("1.0", target_text)

    @staticmethod
    def button_enter(evt):
        evt.widget.config(bg="#84AAFF")

    @staticmethod
    def button_leave(evt):
        evt.widget.config(bg="#649AFA")

    @staticmethod
    def choice_enter(evt):
        evt.widget.config(bg="#3A3A3A")

    @staticmethod
    def choice_leave(evt):
        evt.widget.config(bg="#262626")

    def change_panel(self, panel):
        for i in self.data["panel_list"]:
            self.data["panel_list"][i].place_forget()
        self.data["panel_list"][panel].place(x=160, relwidth=1, width=-160, relheight=1)
