import tkinter
import math
import tkinter.font
import tkinter.ttk


class Window:
    def __init__(self, width=1260, height=900):
        self.window = tkinter.Tk()
        self.window.option_add("*Font", "宋体")
        self.window.title("合同生成器")
        self.window.geometry("%sx%s" % (width, height))
        self.window.minsize(900, 500)
        self.window.configure(bg="#323232")
        self.window.update()
        self.gui_init(self.window)
        self.window.mainloop()

    def gui_init(self, window):
        pass


class MainWindow(Window):
    def __init__(self):
        self.menu_canvas = None
        self.tem_canvas = None
        self.info_frame = None
        self.info_canvas = None
        self.info_menu = None
        self.chosen_file_id = None
        self.setting_button = None
        self.file_list = list()
        self.menu_list = list()
        self.info_list = dict()
        self.now_size = [1260, 900]
        self.detail_data = dict()

        super().__init__()

    def gui_init(self, window):
        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_font.configure(family="黑体", size=15)
        self.window.option_add("*Font", default_font)

        info_canvas = tkinter.Canvas(window, bg="#323232", scrollregion=(0, 0, 0, 1800))
        info_canvas.place(relx=1, x=-500, y=67, width=500, height=-64, relheight=1)
        info_frame = tkinter.Frame(info_canvas, bg="#323232", bd=20, highlightbackground="#323232")
        info_frame.place(x=0, y=0, relwidth=1)
        info_canvas.create_window((0, 0), window=info_frame, anchor="nw")
        menu_canvas = tkinter.Canvas(window, bg="#323232", bd=0, highlightbackground="#454545")
        menu_canvas.place(x=-3, y=0, relwidth=1, width=6, height=70)
        tem_canvas = tkinter.Canvas(window, bg="#262626", bd=0, highlightbackground="#262626")
        tem_canvas.place(x=0, y=70, width=-500, relwidth=1, height=-70, relheight=1)
        self.menu_canvas = menu_canvas
        self.tem_canvas = tem_canvas
        self.info_canvas = info_canvas
        self.info_frame = info_frame

        tem_scr = tkinter.Scrollbar(self.tem_canvas, command=tem_canvas.yview)
        tem_scr.place(x=-16, relx=1, y=0, relheight=1)
        self.tem_canvas.config(yscrollcommand=tem_scr.set)
        info_scr = tkinter.Scrollbar(info_canvas, command=info_canvas.yview)
        info_scr.place(relx=1, x=-16, y=0, relheight=1, height=-73)
        info_canvas.config(yscrollcommand=info_scr.set)

        info_menu = tkinter.Frame(window, bg="#323232")
        info_menu.place(relx=1, x=-498, rely=1, y=-70, width=510, height=75)
        info_menu_frame = tkinter.Frame(info_menu, height=3, bg="#454545")
        info_menu_frame.pack(side="top", fill="x")
        button_disabled_img = tkinter.PhotoImage(file="img/button_disabled.png", width=110, height=50)
        button_enabled_img = tkinter.PhotoImage(file="img/button_enabled.png", width=110, height=50)
        back_disabled_img = tkinter.PhotoImage(file="img/back_disabled.png", width=35, height=35)
        back_enabled_img = tkinter.PhotoImage(file="img/back_enabled.png", width=35, height=35)
        save_disabled_img = tkinter.PhotoImage(file="img/save_disabled.png", width=35, height=35)
        save_enabled_img = tkinter.PhotoImage(file="img/save_enabled.png", width=35, height=35)
        info_menu_create = tkinter.Label(info_menu, width=110, height=50, image=button_enabled_img, text="新建",
                                         bg="#323232", fg="#E4E4E4", compound="center", cursor="hand2")
        info_menu_save = tkinter.Label(info_menu, image=save_disabled_img, bg="#323232", cursor="arrow")
        info_menu_back = tkinter.Label(info_menu, image=back_disabled_img, bg="#323232", cursor="arrow")
        info_menu_create.pack(side="right", padx=15)
        info_menu_save.pack(side="left", padx=10)
        info_menu_back.pack(side="left", padx=0)
        self.info_menu = info_menu
        self.info_list["info_menu_create"] = info_menu_create
        self.info_list["info_menu_save"] = info_menu_save
        self.info_list["info_menu_back"] = info_menu_back
        self.info_list["button_disabled_img"] = button_disabled_img
        self.info_list["button_enabled_img"] = button_enabled_img
        self.info_list["back_disabled_img"] = back_disabled_img
        self.info_list["back_enabled_img"] = back_enabled_img
        self.info_list["save_disabled_img"] = save_disabled_img
        self.info_list["save_enabled_img"] = save_enabled_img

        # 右侧布局代码
        agm_number_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="合同编号:")
        agm_number_entry = tkinter.Text(info_frame, bg="#323232", fg="#A0A0A0", highlightbackground="#323232",
                                        highlightcolor="#323232", bd=0, highlightthickness=1, insertbackground="#323232",
                                        height=1, width=15, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_number_entry.insert("0.0", "<自动>")
        agm_number_entry.config(state="disabled")

        agm_time_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="签订时间:")
        agm_time_frame = tkinter.Frame(info_frame, bg="#323232")
        agm_time_year = tkinter.Text(agm_time_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                     highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                     height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_time_year.insert("0.0", "<自动>")
        agm_time_year.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")
        agm_time_month = tkinter.Text(agm_time_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                      highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                      height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_time_month.insert("0.0", "<自动>")
        agm_time_month.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")
        agm_time_day = tkinter.Text(agm_time_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                   highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                   height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_time_day.insert("0.0", "<自动>")
        agm_time_day.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")
        agm_time_sp01 = tkinter.Label(agm_time_frame, bg="#323232", fg="#A0A0A0", text="年")
        agm_time_sp02 = tkinter.Label(agm_time_frame, bg="#323232", fg="#A0A0A0", text="月")
        agm_time_sp03 = tkinter.Label(agm_time_frame, bg="#323232", fg="#A0A0A0", text="日")
        agm_time_year.grid(row=0, column=0)
        agm_time_sp01.grid(row=0, column=1)
        agm_time_month.grid(row=0, column=2)
        agm_time_sp02.grid(row=0, column=3)
        agm_time_day.grid(row=0, column=4)
        agm_time_sp03.grid(row=0, column=5)
        self.info_list["agm_time_year"] = agm_time_year
        self.info_list["agm_time_month"] = agm_time_month
        self.info_list["agm_time_day"] = agm_time_day

        agm_fnumber_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="编号尾号:")
        agm_fnumber_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                         highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                         insertbackground="#A0A0A0",
                                         height=1, width=8, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_fnumber_entry.insert("0.0", "<自动>")
        agm_fnumber_entry.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")

        agm_supplier_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="供方:")
        agm_supplier_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                          highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                          height=1, width=25, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_demander_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="需方:")
        agm_demander_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                          highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                          height=1, width=25, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        # tkinter.Frame(info_frame, height=25, bg="#323232").grid(column=0, row=0)
        agm_number_label.grid(column=0, row=0, pady=5, sticky=tkinter.W)
        agm_number_entry.grid(column=1, row=0, pady=5, sticky=tkinter.W)
        agm_time_label.grid(column=0, row=1, pady=5, sticky=tkinter.W)
        agm_time_frame.grid(column=1, row=1, pady=5, sticky=tkinter.W)
        agm_fnumber_label.grid(column=0, row=2, pady=5, sticky=tkinter.W)
        agm_fnumber_entry.grid(column=1, row=2, pady=5, sticky=tkinter.W)
        agm_supplier_label.grid(column=0, row=3, pady=5, sticky=tkinter.W)
        agm_supplier_entry.grid(column=1, row=3, pady=5, sticky=tkinter.W)
        agm_demander_label.grid(column=0, row=4, pady=5, sticky=tkinter.W)
        agm_demander_entry.grid(column=1, row=4, pady=5, sticky=tkinter.W)
        self.info_list["agm_fnumber_entry"] = agm_fnumber_entry
        self.info_list["agm_number_entry"] = agm_number_entry
        self.info_list["agm_supplier_entry"] = agm_supplier_entry
        self.info_list["agm_demander_entry"] = agm_demander_entry

        info_detail = tkinter.Frame(self.info_frame, bg="#323232")
        info_detail.grid(column=0, columnspan=2, row=5, pady=15, sticky=tkinter.W)
        info_detail_text = tkinter.Label(info_detail, bg="#323232", fg="#649AFA", font="黑体 13", text="合同详情")
        line_close = tkinter.PhotoImage(file="img/line_close.png", width=300, height=19)
        line_open = tkinter.PhotoImage(file="img/line_open.png", width=300, height=19)
        arrow_open = tkinter.PhotoImage(file="img/arrow_open.png", width=19, height=19)
        arrow_close = tkinter.PhotoImage(file="img/arrow_close.png", width=19, height=19)
        info_detail_line = tkinter.Label(info_detail, bg="#323232", image=line_open, width=300)
        info_detail_button = tkinter.Label(info_detail, bg="#323232", image=arrow_open, cursor="hand2")
        info_detail_text.grid(row=0, column=0, sticky=tkinter.W)
        info_detail_line.grid(row=0, column=1)
        info_detail_button.grid(row=0, column=2)
        info_inner_detail = tkinter.Frame(info_detail, bg="#323232")
        info_inner_detail.grid(row=1, column=0, columnspan=3, pady=5, sticky=tkinter.W)

        self.detail_data["info"] = 1

        def info_detail(evt):
            if self.detail_data["info"] == 0:
                self.detail_data["info"] = 1
                self.info_list["info_detail_text"].config(fg="#649AFA")
                self.info_list["info_detail_line"].config(image=self.info_list["line_open"])
                self.info_list["info_detail_button"].config(image=self.info_list["arrow_open"])
                self.info_list["info_inner_detail"].grid(row=1, column=0, columnspan=3, pady=5, sticky=tkinter.W)
            else:
                self.detail_data["info"] = 0
                self.info_list["info_detail_text"].config(fg="#7A7A7A")
                self.info_list["info_detail_line"].config(image=self.info_list["line_close"])
                self.info_list["info_detail_button"].config(image=self.info_list["arrow_close"])
                self.info_list["info_inner_detail"].grid_forget()

        info_detail_button.bind("<Button-1>", info_detail)

        label_list = ["品牌", "交(提)货时间", "交(提)货地点", "结算方式\n及期限", "备注", "其他约定事情\n①",
                      "其他约定事情\n②", "其他约定事情\n③", "其他约定事情\n④", "其他约定事情\n⑤", "其他约定事情\n⑥"]
        setting_list = [(1, 15), (1, 15), (1, 27), (3, 27), (1, 27), (5, 27), (5, 27), (5, 27), (5, 27), (5, 27), (5, 27)]
        for i in range(len(label_list)):
            require_label = tkinter.Label(info_inner_detail, bg="#323232", fg="#909090", text=label_list[i],
                                          font="黑体 13", justify="left")
            require_entry = tkinter.Text(info_inner_detail, bg="#464646", fg="#909090", highlightbackground="#A0A0A0",
                                         highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                         insertbackground="#A0A0A0", height=setting_list[i][0], width=setting_list[i][1],
                                         wrap="char", undo=True, maxundo=-1, padx=10, pady=5,
                                         font="宋体 13")
            require_label.grid(row=i, column=0, sticky=tkinter.W + tkinter.N, ipadx=10, pady=5)
            require_entry.grid(row=i, column=1, sticky=tkinter.W, pady=5)
            self.info_list["info_detail_require%s" % i] = require_entry

        self.info_list["line_close"] = line_close
        self.info_list["line_open"] = line_open
        self.info_list["arrow_open"] = arrow_open
        self.info_list["arrow_close"] = arrow_close
        self.info_list["info_inner_detail"] = info_inner_detail
        self.info_list["info_detail_button"] = info_detail_button
        self.info_list["info_detail_line"] = info_detail_line
        self.info_list["info_detail_text"] = info_detail_text

        supplier_detail = tkinter.Frame(self.info_frame, bg="#323232")
        supplier_detail.grid(column=0, columnspan=2, row=6, pady=15, sticky=tkinter.W)
        supplier_detail_text = tkinter.Label(supplier_detail, bg="#323232", fg="#649AFA", font="黑体 13", text="供方详情")
        supplier_detail_line = tkinter.Label(supplier_detail, bg="#323232", image=line_open, width=300)
        supplier_detail_button = tkinter.Label(supplier_detail, bg="#323232", image=arrow_open, cursor="hand2")
        supplier_detail_text.grid(row=0, column=0, sticky=tkinter.W)
        supplier_detail_line.grid(row=0, column=1)
        supplier_detail_button.grid(row=0, column=2)
        supplier_inner_detail = tkinter.Frame(supplier_detail, bg="#323232")
        supplier_inner_detail.grid(row=1, column=0, columnspan=3, pady=5, sticky=tkinter.W)

        self.detail_data["supplier"] = 1

        def supplier_detail(evt):
            if self.detail_data["supplier"] == 0:
                self.detail_data["supplier"] = 1
                self.info_list["supplier_detail_text"].config(fg="#649AFA")
                self.info_list["supplier_detail_line"].config(image=self.info_list["line_open"])
                self.info_list["supplier_detail_button"].config(image=self.info_list["arrow_open"])
                self.info_list["supplier_inner_detail"].grid(row=1, column=0, columnspan=3, pady=5, sticky=tkinter.W)
            else:
                self.detail_data["supplier"] = 0
                self.info_list["supplier_detail_text"].config(fg="#7A7A7A")
                self.info_list["supplier_detail_line"].config(image=self.info_list["line_close"])
                self.info_list["supplier_detail_button"].config(image=self.info_list["arrow_close"])
                self.info_list["supplier_inner_detail"].grid_forget()

        supplier_detail_button.bind("<Button-1>", supplier_detail)

        label_list = ["单位地址", "开户银行", "账号", "税政号码", "电话"]
        setting_list = [(2, 27), (1, 27), (1, 27), (1, 27), (1, 27)]
        for i in range(len(label_list)):
            require_label = tkinter.Label(supplier_inner_detail, bg="#323232", fg="#909090", text=label_list[i],
                                          font="黑体 13", justify="left")
            require_entry = tkinter.Text(supplier_inner_detail, bg="#464646", fg="#909090", highlightbackground="#A0A0A0",
                                         highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                         insertbackground="#A0A0A0", height=setting_list[i][0],
                                         width=setting_list[i][1],
                                         wrap="char", undo=True, maxundo=-1, padx=10, pady=5,
                                         font="宋体 13")
            require_label.grid(row=i, column=0, sticky=tkinter.W + tkinter.N, ipadx=10, pady=5)
            require_entry.grid(row=i, column=1, sticky=tkinter.W, pady=5)
            self.info_list["supplier_detail_require%s" % i] = require_entry

        self.info_list["supplier_inner_detail"] = supplier_inner_detail
        self.info_list["supplier_detail_button"] = supplier_detail_button
        self.info_list["supplier_detail_line"] = supplier_detail_line
        self.info_list["supplier_detail_text"] = supplier_detail_text

        demander_detail = tkinter.Frame(self.info_frame, bg="#323232")
        demander_detail.grid(column=0, columnspan=2, row=7, pady=15, sticky=tkinter.W)
        demander_detail_text = tkinter.Label(demander_detail, bg="#323232", fg="#649AFA", font="黑体 13", text="需方详情")
        demander_detail_line = tkinter.Label(demander_detail, bg="#323232", image=line_open, width=300)
        demander_detail_button = tkinter.Label(demander_detail, bg="#323232", image=arrow_open, cursor="hand2")
        demander_detail_text.grid(row=0, column=0, sticky=tkinter.W)
        demander_detail_line.grid(row=0, column=1)
        demander_detail_button.grid(row=0, column=2)
        demander_inner_detail = tkinter.Frame(demander_detail, bg="#323232")
        demander_inner_detail.grid(row=1, column=0, columnspan=3, pady=5, sticky=tkinter.W)

        self.detail_data["demander"] = 1

        def demander_detail(evt):
            if self.detail_data["demander"] == 0:
                self.detail_data["demander"] = 1
                self.info_list["demander_detail_text"].config(fg="#649AFA")
                self.info_list["demander_detail_line"].config(image=self.info_list["line_open"])
                self.info_list["demander_detail_button"].config(image=self.info_list["arrow_open"])
                self.info_list["demander_inner_detail"].grid(row=1, column=0, columnspan=3, pady=5, sticky=tkinter.W)
            else:
                self.detail_data["demander"] = 0
                self.info_list["demander_detail_text"].config(fg="#7A7A7A")
                self.info_list["demander_detail_line"].config(image=self.info_list["line_close"])
                self.info_list["demander_detail_button"].config(image=self.info_list["arrow_close"])
                self.info_list["demander_inner_detail"].grid_forget()

        demander_detail_button.bind("<Button-1>", demander_detail)

        label_list = ["单位地址", "开户银行", "账号", "税政号码", "电话"]
        setting_list = [(2, 27), (1, 27), (1, 27), (1, 27), (1, 27)]
        for i in range(len(label_list)):
            require_label = tkinter.Label(demander_inner_detail, bg="#323232", fg="#909090", text=label_list[i],
                                          font="黑体 13", justify="left")
            require_entry = tkinter.Text(demander_inner_detail, bg="#464646", fg="#909090",
                                         highlightbackground="#A0A0A0",
                                         highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                         insertbackground="#A0A0A0", height=setting_list[i][0],
                                         width=setting_list[i][1],
                                         wrap="char", undo=True, maxundo=-1, padx=10, pady=5,
                                         font="宋体 13")
            require_label.grid(row=i, column=0, sticky=tkinter.W + tkinter.N, ipadx=10, pady=5)
            require_entry.grid(row=i, column=1, sticky=tkinter.W, pady=5)
            self.info_list["demander_detail_require%s" % i] = require_entry

        self.info_list["demander_inner_detail"] = demander_inner_detail
        self.info_list["demander_detail_button"] = demander_detail_button
        self.info_list["demander_detail_line"] = demander_detail_line
        self.info_list["demander_detail_text"] = demander_detail_text

        for i in range(15):
            self.add_agm("D:/test/test/合同1.agm")
        self.chosen_file_id = self.file_list[0]["id_number"]
        self.choose_file(self.file_list[0]["id_number"])

        menu_name = ["合同模板", "最近打开", "全部", "收藏"]
        menu_icon = ["tem_icon.png", "recent_icon.png", "all_icon.png", "collect_icon.png"]
        length = 0
        for i in range(len(menu_name)):
            now_length = len(menu_name[i]) * 15 + 90
            frame = self.menu_canvas.create_rectangle(length, 0, length + now_length, 70, outline="")
            select_sign = self.menu_canvas.create_rectangle(length, 65, length + now_length, 70, outline="",
                                                            fill="")
            icon_file = tkinter.PhotoImage(file="img/" + menu_icon[i], width=35, height=35)
            icon = self.menu_canvas.create_image(length + 35, 35, image=icon_file)
            text = self.menu_canvas.create_text(length + 60, 35, text=menu_name[i], fill="#A0A0A0", font="黑体 14",
                                                anchor="w")
            menu_dict = {"icon_file": icon_file, "icon": icon, "frame": frame, "text": text, "select_sign": select_sign,
                         "id": i}
            length += now_length

            for i2 in menu_dict:
                if i2 != "id":
                    self.menu_canvas.tag_bind(menu_dict[i2], "<Enter>", self.get_menu_enter(i))
                    self.menu_canvas.tag_bind(menu_dict[i2], "<Leave>", self.get_menu_leave(i))
                    self.menu_canvas.tag_bind(menu_dict[i2], "<Button-1>", self.get_menu_click(i))

            self.menu_list.append(menu_dict)

        setting_img = tkinter.PhotoImage(file="img/setting_icon.png", width=35, height=35)
        self.setting_button = tkinter.Label(window, image=setting_img, bg="#323232", cursor="hand2")
        self.setting_button.place(relx=1, x=-50, y=15)
        self.info_list["setting_img"] = setting_img

        self.get_menu_click(0)(None)
        self.info_frame.update()

        self.window.bind("<Configure>", self.size_change)
        self.tem_canvas.bind("<MouseWheel>", self.canvas_wheel)
        self.info_canvas.bind("<MouseWheel>", self.canvas_wheel)
        for i in self.info_list:
            if type(self.info_list[i]) is tkinter.Entry or type(self.info_list[i]) is tkinter.Text:
                self.info_list[i].bind("<KeyPress>", self.info_change)

    def choose_file(self, file_id):
        self.info_list["info_menu_save"].config(image=self.info_list["save_disabled_img"], cursor="arrow")
        self.info_list["info_menu_back"].config(image=self.info_list["back_disabled_img"], cursor="arrow")
        for i in self.file_list:
            if i["id_number"] == file_id:
                self.tem_canvas.itemconfigure(i["frame"], width=3, outline="#649AFA")
                self.tem_canvas.itemconfigure(i["agm_name"], fill="#898989")
            else:
                self.tem_canvas.itemconfigure(i["frame"], width=2, outline="#454545")
                self.tem_canvas.itemconfigure(i["agm_name"], fill="#898989")

    def info_change(self, evt):
        self.info_list["info_menu_save"].config(image=self.info_list["save_enabled_img"], cursor="hand2")
        self.info_list["info_menu_back"].config(image=self.info_list["back_enabled_img"], cursor="hand2")

    def get_menu_enter(self, menu_id=0):
        def func(evt):
            self.menu_enter(menu_id)
        return func

    def get_menu_leave(self, menu_id=0):
        def func(evt):
            self.menu_leave(menu_id)
        return func

    def get_menu_click(self, menu_id=0):
        def func(evt):
            self.menu_click(menu_id)
        return func

    def menu_enter(self, menu_id):
        self.menu_canvas.configure(cursor="hand2")
        for i in self.menu_list:
            if i["id"] == menu_id:
                self.menu_canvas.itemconfigure(i["frame"], width=5, fill="#3A3A3A")
                self.menu_canvas.itemconfigure(i["text"], fill="#649AFA")
                break

    def menu_leave(self, menu_id):
        self.menu_canvas.configure(cursor="arrow")
        for i in self.menu_list:
            if i["id"] == menu_id:
                self.menu_canvas.itemconfigure(i["frame"], width=5, fill="")
                self.menu_canvas.itemconfigure(i["text"], fill="#A0A0A0")
                break

    def menu_click(self, menu_id):
        for i in self.menu_list:
            self.menu_canvas.itemconfigure(i["select_sign"], fill="")
        for i in self.menu_list:
            if i["id"] == menu_id:
                self.menu_canvas.itemconfigure(i["select_sign"], fill="#649AFA")
                break

    def size_change(self, evt):
        if self.window.winfo_width() != self.now_size[0] or self.window.winfo_height() != self.now_size[1]:
            self.now_size[0] = self.window.winfo_width()
            self.now_size[1] = self.window.winfo_height()
            now_length = 0
            for i in self.file_list:
                line_contain = math.floor((self.window.winfo_width() - 530) / 180)
                line = now_length // line_contain
                column = now_length % line_contain
                x = column * 180 + 20
                y = line * 180 + 20
                now_length += 1
                if y + 300 < self.window.winfo_height() - 74:
                    self.tem_canvas.configure(scrollregion=(0, 0, 0, self.window.winfo_height() - 74))
                else:
                    self.tem_canvas.configure(scrollregion=(0, 0, 0, y + 300))

                self.tem_canvas.coords(i["frame"], x, y, x + 160, y + 160)
                self.tem_canvas.coords(i["agm_img"], x + 80, y + 70)
                self.tem_canvas.coords(i["agm_number"], x + 80, y + 83)
                self.tem_canvas.coords(i["agm_name"], x + 80, y + 135)

    def file_enter(self, id_number):
        for i in self.file_list:
            if i["id_number"] == id_number and id_number != self.chosen_file_id:
                self.tem_canvas.configure(cursor="hand2")
                self.tem_canvas.itemconfigure(i["frame"], width=5, fill="#3A3A3A")
                self.tem_canvas.itemconfigure(i["agm_name"], font="黑体 15", fill="#649AFA")
                break
            elif i["id_number"] == id_number and id_number == self.chosen_file_id:
                self.tem_canvas.configure(cursor="hand2")
                self.tem_canvas.itemconfigure(i["frame"], width=5)
                break

    def file_leave(self, id_number):
        for i in self.file_list:
            if i["id_number"] == id_number and id_number != self.chosen_file_id:
                self.tem_canvas.configure(cursor="arrow")
                self.tem_canvas.itemconfigure(i["frame"], width=2, fill="#323232")
                self.tem_canvas.itemconfigure(i["agm_name"], font="黑体 13", fill="#898989")
                break
            elif i["id_number"] == id_number and id_number == self.chosen_file_id:
                self.tem_canvas.configure(cursor="arrow")
                self.tem_canvas.itemconfigure(i["frame"], width=3)
                break

    def file_click(self, id_number):
        self.chosen_file_id = id_number
        self.choose_file(id_number)

    def add_agm(self, path, number="21070821", img="img/agreement_file.png", width=100, height=100, agm_type="file"):
        now_length = len(self.file_list)
        line_contain = math.floor((self.window.winfo_width() - 530) / 180)
        line = now_length // line_contain
        column = now_length % line_contain
        x = column * 180 + 20
        y = line * 180 + 20
        name = path.split("/")[-1].split(".")[0]
        if y + 300 < self.window.winfo_height() - 74:
            self.tem_canvas.configure(scrollregion=(0, 0, 0, self.window.winfo_height() - 74))
        else:
            self.tem_canvas.configure(scrollregion=(0, 0, 0, y + 300))

        frame = self.tem_canvas.create_rectangle(x, y, x + 160, y + 160, fill="#323232", outline="#454545", width=2)
        img_file = tkinter.PhotoImage(file=img, width=width, height=height)
        agm_img = self.tem_canvas.create_image(x + 80, y + 70, image=img_file)
        agm_number = self.tem_canvas.create_text(x + 80, y + 83, text=number, fill="#323232", font="华文琥珀 9")
        agm_name = self.tem_canvas.create_text(x + 80, y + 135, text=name, fill="#898989", font="黑体 13")
        id_number = len(self.file_list)

        agm_dict = {"img_file": img_file, "agm_img": agm_img, "frame": frame, "agm_number": agm_number,
                    "agm_name": agm_name, "id_number": id_number, "type": agm_type}

        def file_enter_id(event):
            self.file_enter(id_number)

        def file_leave_id(event):
            self.file_leave(id_number)

        def file_click_id(event):
            self.file_click(id_number)

        for i in agm_dict:
            if i != "id_number" and i != "type":
                self.tem_canvas.tag_bind(agm_dict[i], "<Enter>", file_enter_id)
                self.tem_canvas.tag_bind(agm_dict[i], "<Leave>", file_leave_id)
                self.tem_canvas.tag_bind(agm_dict[i], "<Button-1>", file_click_id)
        self.file_list.append(agm_dict)

    def frame_wheel(self, evt):
        if evt.delta > 0:
            self.info_canvas.yview("scroll", -3, "units")
        elif evt.delta < 0:
            self.info_canvas.yview("scroll", 3, "units")

    @staticmethod
    def canvas_wheel(evt):
        if evt.delta > 0:
            evt.widget.yview("scroll", -3, "units")
        elif evt.delta < 0:
            evt.widget.yview("scroll", 3, "units")


if __name__ == "__main__":
    main_window = MainWindow()
