import tkinter
import math
import tkinter.font
import tkinter.ttk


class MultipleBar:
    def __init__(self, master, bg, width=None, event=None, **data):
        self.data = data
        self.event = event
        self.items = list()
        self.display_list = list()
        if width is None:
            self.canvas = tkinter.Canvas(master=master, bg=bg, bd=0, highlightbackground=bg, height=30)
        else:
            self.canvas = tkinter.Canvas(master=master, bg=bg, bd=0, highlightbackground=bg, height=30, width=width)
        self.gui_init()

    def gui_init(self):
        pass

    def draw(self):
        pass

    def add_item(self, name):
        if name not in self.items:
            self.items.append(name)
            self.draw()

    def delete_item(self, name):
        self.items.remove(name)
        self.draw()

    def get_canvas(self):
        return self.canvas


class StandardBar(MultipleBar):
    def gui_init(self):
        self.canvas.configure(scrollregion=(0, 0, 1300, 0))
        self.canvas.bind("<MouseWheel>", self.canvas_move)
        self.draw()

    def canvas_move(self, evt):
        self.canvas.configure(cursor="arrow")
        if evt.delta > 0:
            self.canvas.xview("scroll", 1, "units")
        else:
            self.canvas.xview("scroll", -1, "units")

    def draw(self):
        self.canvas.delete("all")
        self.canvas.configure(cursor="arrow")
        now_x = 120
        for i in self.items:
            name = i[0] if i[1] == 0 else "%s|%s" % (i[0], i[1])
            length = 0
            for char in name:
                if u'\u4e00' <= char <= u'\u9fff':
                    length += 19
                else:
                    length += 9.5
            length += 20
            rect = self.canvas.create_rectangle((now_x - 10, 0, now_x + 10 + length, 35), width=0, fill="#649AFA")
            text = self.canvas.create_text((now_x, 17), text=name, font="宋体 14", anchor="w", fill="#E4E4E4")
            delete = self.canvas.create_text((now_x + length - 15, 17), text="×", font="黑体 14", anchor="w",
                                             fill="#E4E4E4")
            delete_func = self.get_mouse_func(i[0])
            self.canvas.tag_bind(delete, "<Enter>", self.mouse_enter)
            self.canvas.tag_bind(delete, "<Leave>", self.mouse_leave)
            self.canvas.tag_bind(delete, "<Button-1>", delete_func)
            now_x += length + 30
        self.canvas.create_rectangle((0, 0, 100, 35), width=0, fill="#323232")
        self.canvas.create_rectangle((0, 0, 5, 35), width=0, fill="#649AFA")
        self.canvas.create_text((10, 17), text="全部附加:", font="黑体 14", anchor="w", fill="#9A9A9A")
        mouse_wheel_img = tkinter.PhotoImage(file="img/mouse_wheel.png", width=25, height=25)
        wheel = self.canvas.create_image((now_x, 17.5), image=mouse_wheel_img)
        self.canvas.tag_bind(wheel, "<Enter>", self.mouse_enter_special)
        self.canvas.tag_bind(wheel, "<Leave>", self.mouse_leave)
        self.data["mouse_wheel_img"] = mouse_wheel_img

    def get_mouse_func(self, name):
        def mouse_event(evt):
            self.delete(name)
        return mouse_event

    def add_item(self, name, price=0):
        for i in self.items:
            if i[0] == name:
                return False
        self.items.append((name, price))
        self.draw()
        return True

    def delete(self, name):
        self.delete_item(name=name)

    def delete_item(self, name):
        for i in self.items:
            if i[0] == name:
                self.items.remove(i)
                break
        self.draw()

    def mouse_enter_special(self, evt):
        self.canvas.configure(cursor="sb_h_double_arrow")

    def mouse_enter(self, evt):
        self.canvas.configure(cursor="hand2")

    def mouse_leave(self, evt):
        self.canvas.configure(cursor="arrow")

    def get_items(self):
        return self.items


class Window:
    def __init__(self, width=1260, height=900):
        self.window = tkinter.Tk()
        self.window.option_add("*Font", "黑体 15")
        self.window.title("合同生成器")
        self.window.geometry("%sx%s" % (width, height))
        self.window.minsize(900, 500)
        self.window.configure(bg="#323232")
        self.window.update()
        self.gui_init(self.window)
        self.window.mainloop()

    def gui_init(self, window):
        pass


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


class ChildWindow:
    count = 0

    @staticmethod
    def check():
        return __class__.count == 0

    def __init__(self, master, width=1260, height=900, minsize_x=400, minsize_y=400, resizable=False):
        if self.check():
            __class__.count += 1
            self.window = tkinter.Toplevel(master=master)
            self.window.option_add("*Font", "黑体 15")
            self.window.title("合同生成器")
            self.window.resizable(width=resizable, height=resizable)
            self.window.geometry("%sx%s" % (width, height))
            self.window.minsize(minsize_x, minsize_y)
            self.window.configure(bg="#323232")
            self.window.update()
            self.window.protocol("WM_DELETE_WINDOW", self.close)
            self.data = dict()
            self.gui_init(self.window)
            self.window.mainloop()

    def close(self):
        __class__.count -= 1
        self.window.destroy()

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

        self.setting_button.bind("<Button-1>", self.open_setting_menu)
        self.window.bind("<Configure>", self.size_change)
        self.tem_canvas.bind("<MouseWheel>", self.canvas_wheel)
        self.info_canvas.bind("<MouseWheel>", self.canvas_wheel)
        for i in self.info_list:
            if type(self.info_list[i]) is tkinter.Entry or type(self.info_list[i]) is tkinter.Text:
                self.info_list[i].bind("<KeyPress>", self.info_change)

    def open_setting_menu(self, evt):
        setting_menu = SettingWindow(master=self.window, width=1280, height=800, resizable=True)

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


class SettingWindow(ChildWindow):
    def gui_init(self, window):
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
        base_setting_label = tkinter.Label(base_setting_frame, text="无可用设置", font="黑体 25", fg="#646464",
                                           bg="#323232")
        base_setting_label.pack()
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
                                             height=1, width=4, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
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
        tkinter.Label(product_line01, bg="#464646", fg="#A0A0A0", text="A", font="黑体 14", padx=3).pack(side="left")
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
        product_search_button = tkinter.Label(product_detail_line01, bg="#464646", image=search_image)
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
        test_name = ["智能型万能式断路器", "智能型万能式断路器", "微型断路器", "塑壳断路器", "高压真空断路器"]
        test_type = ["RMW1-2000S/3P", "RMW2-2000S/3P", "RMC3-125", "RMM3-630S/3300", "RMVS1-12/630-25"]
        test_adjunct = ["RMW1-2000S/3P 1250 抽屉式 bse4 控制电压:AC230V +门框 +相间隔板+配4组转换辅助触头",
                        "RMW1-2000S/4P 1250 抽屉式 bse4 控制电压:AC230V +门框 +相间隔板+配4组转换辅助触头/延时欠电压脱扣器AC230V延时3S+2合1缆绳联锁",
                        "", "分励AC220V", "相距210mm 固定式 合/分闸线圈/储能电机AC220V 闭锁线圈"]
        test_price = ["16700", "21700", "330", "210", "16000"]
        test_adjunctPrice = ["80", "80", "0", "0", "0"]

        def select(event):
            selection = product_list_box.selection()
            id_list = self.data["product_id_list"]
            for i in id_list:
                if i in selection:
                    product_list_box.tag_configure(i, background="#649AFA", foreground="#E4E4E4")
                else:
                    product_list_box.tag_configure(i, background="#323232", foreground="#A0A0A0")

        product_list_box.bind('<<TreeviewSelect>>', select)
        self.data["product_treeview"] = product_list_box
        self.data["product_id_list"] = list()
        self.product_list_set(test_name, test_type, test_adjunct, test_price, test_adjunctPrice)

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
        product_detail_line02.pack(side="bottom", fill="x")
        tkinter.Frame(product_detail_frame, bg="#464646", height=20).pack(side="top")
        product_listbox_scroll.pack(side="right", fill="y")
        product_list_box.pack(side="top", fill="both", expand=1)

        widget_list["screen_name_cb"] = screen_name_cb
        widget_list["screen_type_cb"] = screen_type_cb
        widget_list["product_list_delete"] = product_list_delete
        widget_list["product_delete_lock"] = product_delete_lock

        screen_name_cb.bind("<<ComboboxSelected>>", self.screen_name_change)
        product_delete_lock.bind("<Button-1>", self.lock_change)
        # product_list_delete.bind("<Button-1>", self.delete_product)

    def product_list_set(self, name_list, type_list, adjunct_list, price_list, adjunctPrice_list):
        product_id_list = list()
        for i in range(len(name_list)):
            id_tag = "I{:0>3}".format(i + 1)
            product_id_list.append(id_tag)
            self.data["product_treeview"].insert('', i,
                                                 values=(name_list[i], type_list[i], adjunct_list[i], price_list[i],
                                                         adjunctPrice_list[i]), tags=(id_tag, "all"))
        self.data["product_id_list"] = product_id_list

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

    def delete_product(self, evt):
        pass

    def add_product(self, evt):
        pass

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

    def screen_name_change(self, evt):
        choice = self.data["widget_list"]["screen_name_cb"].get()
        keys = list(product_type[choice]) if choice != "全部" else list()
        keys.insert(0, "全部")
        self.data["widget_list"]["screen_type_cb"]["value"] = keys
        self.data["widget_list"]["screen_type_cb"].current(0)

    def product_name_change(self, evt):
        choice = self.data["widget_list"]["product_name_cb"].get()
        self.data["widget_list"]["product_type_cb"]["value"] = tuple(product_type[choice])
        self.data["widget_list"]["product_type_cb"].current(0)

    def add_adjunct(self, evt):
        name = self.data["widget_list"]["product_adjunctName_entry"].get("1.0", 'end-1c')
        name = name.replace("\n", "")
        price = self.data["widget_list"]["product_adjunctPrice_entry"].get("1.0", 'end-1c')
        price = int(price) if price != "" else 0
        if name != "" and self.data["widget_list"]["product_standard_canvas"].add_item(name, price):
            self.data["widget_list"]["product_adjunctName_entry"].delete("0.0", "end")
            self.data["widget_list"]["product_adjunctPrice_entry"].delete("0.0", "end")

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


if __name__ == "__main__":
    main_window = MainWindow()
