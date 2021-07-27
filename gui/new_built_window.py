import tkinter
from child_window import ChildWindow
from tkinter import font


class NewBuiltWindow(ChildWindow):
    new_built_count = 0

    def __init__(self, master, template, width=500, height=800, minsize_x=400, minsize_y=400, title="新建合同",
                 resizable=False):
        self.template = template
        self.info_list = dict()
        self.detail_data = dict()
        self.info_frame = None
        self.info_canvas = None
        self.warning_frame = None
        super().__init__(master, width, height, minsize_x, minsize_y, resizable, title)

    def gui_init(self, window):
        __class__.new_built_count += 1

        info_canvas = tkinter.Canvas(window, bg="#323232", scrollregion=(0, 0, 0, 1850), highlightbackground="#323232")
        info_canvas.place(relx=0, x=0, y=0, width=500, height=0, relheight=1)
        info_frame = tkinter.Frame(info_canvas, bg="#323232", bd=20, highlightbackground="#323232")
        info_frame.place(x=0, y=0, relwidth=1)
        info_canvas.create_window((0, 0), window=info_frame, anchor="nw")
        menu_frame = tkinter.Frame(window, bg="#323232")
        menu_frame.place(rely=1, y=-70, height=70, relwidth=1)
        button_disabled_img = tkinter.PhotoImage(file="img/button_disabled.png", width=110, height=50)
        button_enabled_img = tkinter.PhotoImage(file="img/button_enabled.png", width=110, height=50)
        sure_button = tkinter.Label(menu_frame, width=110, height=50, image=button_disabled_img, text="确定",
                                    bg="#323232", fg="#E4E4E4", compound="center", cursor="arrow")
        cancel_button = tkinter.Label(menu_frame, text="取消", bg="#323232", fg="#646464", cursor="hand2")
        cancel_font = font.Font(cancel_button, cancel_button.cget("font"))
        cancel_font.configure(underline=True)
        cancel_button.configure(font=cancel_font)
        sure_button.pack(side="right", padx=20)
        cancel_button.pack(side="left", padx=20)

        warning_frame = tkinter.Frame(window, bg="#262626")
        tkinter.Label(warning_frame, text="请先确认所有信息无误", font="黑体 13", fg="#A0A0A0", bg="#262626").pack(expand=1)

        def show_warning(evt):
            warning_frame.place(relx=1, x=-240, width=210, rely=1, y=-140, height=60)

        def hide_warning(evt):
            warning_frame.place_forget()

        def cancel_click(evt):
            self.close()

        cancel_button.bind("<Button-1>", cancel_click)
        sure_button.bind("<Enter>", show_warning)
        sure_button.bind("<Leave>", hide_warning)

        self.data["button_disabled_img"] = button_disabled_img
        self.data["button_enabled_img"] = button_enabled_img

        def wheel(evt):
            if evt.delta > 0:
                evt.widget.yview("scroll", -3, "units")
            else:
                evt.widget.yview("scroll", 3, "units")

        info_canvas.bind("<MouseWheel>", wheel)

        info_scr = tkinter.Scrollbar(info_canvas, command=info_canvas.yview)
        info_scr.place(relx=1, x=-16, y=0, relheight=1, height=-73)
        info_canvas.config(yscrollcommand=info_scr.set)

        self.info_frame = info_frame
        self.info_canvas = info_canvas

        # 布局代码
        agm_name_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="合同名:")
        agm_name_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                      highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                      height=1, width=20, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)

        agm_number_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="合同编号:")
        agm_number_entry = tkinter.Text(info_frame, bg="#323232", fg="#A0A0A0", highlightbackground="#323232",
                                        highlightcolor="#323232", bd=0, highlightthickness=1,
                                        insertbackground="#323232",
                                        height=1, width=20, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_number_entry.insert("0.0", "<日期、尾号填写有误>")
        agm_number_entry.config(state="disabled")

        agm_time_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="签订时间:")
        agm_time_frame = tkinter.Frame(info_frame, bg="#323232")
        agm_time_year = tkinter.Text(agm_time_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                     highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                     height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        # agm_time_year.insert("0.0", "<自动>")
        # agm_time_year.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")
        agm_time_month = tkinter.Text(agm_time_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                      highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                      height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        # agm_time_month.insert("0.0", "<自动>")
        # agm_time_month.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")
        agm_time_day = tkinter.Text(agm_time_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                    highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                    height=1, width=6, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        # agm_time_day.insert("0.0", "<自动>")
        # agm_time_day.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")
        agm_time_sp01 = tkinter.Label(agm_time_frame, bg="#323232", fg="#A0A0A0", text="年")
        agm_time_sp02 = tkinter.Label(agm_time_frame, bg="#323232", fg="#A0A0A0", text="月")
        agm_time_sp03 = tkinter.Label(agm_time_frame, bg="#323232", fg="#A0A0A0", text="日")
        agm_time_year.grid(row=0, column=0)
        agm_time_sp01.grid(row=0, column=1)
        agm_time_month.grid(row=0, column=2)
        agm_time_sp02.grid(row=0, column=3)
        agm_time_day.grid(row=0, column=4)
        agm_time_sp03.grid(row=0, column=5)
        self.info_list["agm_name_entry"] = agm_name_entry
        self.info_list["agm_time_year"] = agm_time_year
        self.info_list["agm_time_month"] = agm_time_month
        self.info_list["agm_time_day"] = agm_time_day

        agm_fnumber_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="编号尾号:")
        agm_fnumber_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                         highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                         insertbackground="#A0A0A0",
                                         height=1, width=8, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        # agm_fnumber_entry.insert("0.0", "<自动>")
        # agm_fnumber_entry.config(state="disabled", highlightbackground="#323232", highlightcolor="#323232")

        agm_supplier_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="供方:")
        agm_supplier_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                          highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                          insertbackground="#A0A0A0",
                                          height=1, width=25, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_demander_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="需方:")
        agm_demander_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                          highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                          insertbackground="#A0A0A0",
                                          height=1, width=25, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        # tkinter.Frame(info_frame, height=25, bg="#323232").grid(column=0, row=0)
        agm_number_label.grid(column=0, row=0, pady=5, sticky=tkinter.W)
        agm_number_entry.grid(column=1, row=0, pady=5, sticky=tkinter.W)
        agm_name_label.grid(column=0, row=1, pady=5, sticky=tkinter.W)
        agm_name_entry.grid(column=1, row=1, pady=5, sticky=tkinter.W)
        agm_time_label.grid(column=0, row=2, pady=5, sticky=tkinter.W)
        agm_time_frame.grid(column=1, row=2, pady=5, sticky=tkinter.W)
        agm_fnumber_label.grid(column=0, row=3, pady=5, sticky=tkinter.W)
        agm_fnumber_entry.grid(column=1, row=3, pady=5, sticky=tkinter.W)
        agm_supplier_label.grid(column=0, row=4, pady=5, sticky=tkinter.W)
        agm_supplier_entry.grid(column=1, row=4, pady=5, sticky=tkinter.W)
        agm_demander_label.grid(column=0, row=5, pady=5, sticky=tkinter.W)
        agm_demander_entry.grid(column=1, row=5, pady=5, sticky=tkinter.W)
        self.info_list["agm_fnumber_entry"] = agm_fnumber_entry
        self.info_list["agm_number_entry"] = agm_number_entry
        self.info_list["agm_supplier_entry"] = agm_supplier_entry
        self.info_list["agm_demander_entry"] = agm_demander_entry

        info_detail = tkinter.Frame(self.info_frame, bg="#323232")
        info_detail.grid(column=0, columnspan=2, row=6, pady=15, sticky=tkinter.W)
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

        label_list = ["签订地点", "品牌", "交(提)货时间", "交(提)货地点", "结算方式\n及期限", "备注", "其他约定事情\n①",
                      "其他约定事情\n②", "其他约定事情\n③", "其他约定事情\n④", "其他约定事情\n⑤", "其他约定事情\n⑥"]
        setting_list = [(1, 15), (1, 15), (1, 15), (1, 27), (3, 27), (1, 27), (5, 27), (5, 27), (5, 27), (5, 27),
                        (5, 27), (5, 27)]
        for i in range(len(label_list)):
            require_label = tkinter.Label(info_inner_detail, bg="#323232", fg="#909090", text=label_list[i],
                                          font="黑体 13", justify="left")
            require_entry = tkinter.Text(info_inner_detail, bg="#464646", fg="#909090", highlightbackground="#A0A0A0",
                                         highlightcolor="#649AFA", bd=0, highlightthickness=1,
                                         insertbackground="#A0A0A0", height=setting_list[i][0],
                                         width=setting_list[i][1],
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
        supplier_detail.grid(column=0, columnspan=2, row=7, pady=15, sticky=tkinter.W)
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
            require_entry = tkinter.Text(supplier_inner_detail, bg="#464646", fg="#909090",
                                         highlightbackground="#A0A0A0",
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
        demander_detail.grid(column=0, columnspan=2, row=8, pady=15, sticky=tkinter.W)
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

        def entry_focus(evt):
            evt.widget.config(highlightbackground="#A0A0A0", bg="#464646")
            evt.widget.unbind("<FocusIn>")
            for item in self.info_list:
                if (type(self.info_list[item]) is tkinter.Text or type(self.info_list[item]) is tkinter.Entry) \
                        and item != "agm_number_entry":
                    if self.info_list[item].cget("highlightbackground") == "#D96C6C":
                        return
            sure_button.configure(cursor="hand2", image=button_enabled_img)
            sure_button.unbind("<Enter>")
            sure_button.unbind("<Leave>")

        for i in self.info_list:
            if (type(self.info_list[i]) is tkinter.Text or type(self.info_list[i]) is tkinter.Entry)\
                    and i != "agm_number_entry":
                self.info_list[i].config(highlightbackground="#D96C6C", bg="#3A3A3A")
                self.info_list[i].bind("<FocusIn>", entry_focus)

    @staticmethod
    def check():
        return __class__.new_built_count < 1

    def close(self):
        __class__.new_built_count -= 1
        super().close()
