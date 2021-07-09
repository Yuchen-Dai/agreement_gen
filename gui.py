import tkinter
import math
import tkinter.font


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
        self.file_list = list()
        self.menu_list = list()
        self.now_size = [1260, 900]

        super().__init__()

    def gui_init(self, window):
        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_font.configure(family="黑体", size=15)
        self.window.option_add("*Font", default_font)

        menu_canvas = tkinter.Canvas(window, bg="#323232", bd=0, highlightbackground="#454545")
        menu_canvas.place(x=-3, y=0, relwidth=1, width=6, height=70)
        tem_canvas = tkinter.Canvas(window, bg="#262626", bd=0, highlightbackground="#262626")
        tem_canvas.place(x=0, y=70, width=-500, relwidth=1, height=-70, relheight=1)
        info_frame = tkinter.Frame(window, bg="#323232", bd=20, highlightbackground="#323232")
        info_frame.place(relx=1, x=-500, y=70, width=500, height=-70, relheight=1)
        self.menu_canvas = menu_canvas
        self.tem_canvas = tem_canvas
        self.info_frame = info_frame

        tem_scr = tkinter.Scrollbar(self.tem_canvas, command=tem_canvas.yview)
        tem_scr.place(x=-16, relx=1, y=0, relheight=1)
        self.tem_canvas.config(yscrollcommand=tem_scr.set)

        agm_type_label = tkinter.Label(info_frame, bg="#323232", fg="#A0A0A0", text="合同类型:")
        agm_type_entry = tkinter.Text(info_frame, bg="#464646", fg="#A0A0A0", highlightbackground="#A0A0A0",
                                      highlightcolor="#649AFA", bd=0, highlightthickness=1, insertbackground="#A0A0A0",
                                      height=1, width=20, wrap="none", undo=True, maxundo=-1, padx=10, pady=5)
        agm_type_label.grid(column=0, row=0)
        agm_type_entry.grid(column=1, row=0)

        for i in range(8):
            self.add_agm("D:/test/test/合同1.agm")

        menu_name = ["合同模板", "最近打开", "收藏"]
        menu_icon = ["tem_icon.png", "recent_icon.png", "collect_icon.png"]
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

        self.get_menu_click(0)(None)

        self.window.bind("<Configure>", self.size_change)
        self.tem_canvas.bind("<MouseWheel>", self.tem_wheel)

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
                self.menu_canvas.itemconfigure(i["select_sign"], fill="#A0A0A0")
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
            if i["id_number"] == id_number:
                self.tem_canvas.configure(cursor="hand2")
                self.tem_canvas.itemconfigure(i["frame"], width=5, fill="#3A3A3A")
                self.tem_canvas.itemconfigure(i["agm_name"], font="黑体 15", fill="#649AFA")
                break

    def file_leave(self, id_number):
        for i in self.file_list:
            if i["id_number"] == id_number:
                self.tem_canvas.configure(cursor="arrow")
                self.tem_canvas.itemconfigure(i["frame"], width=2, fill="#323232")
                self.tem_canvas.itemconfigure(i["agm_name"], font="黑体 13", fill="#898989")
                break

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

        for i in agm_dict:
            if i != "id_number" and i != "type":
                self.tem_canvas.tag_bind(agm_dict[i], "<Enter>", file_enter_id)
                self.tem_canvas.tag_bind(agm_dict[i], "<Leave>", file_leave_id)
        self.file_list.append(agm_dict)

    def tem_wheel(self, evt):
        if evt.delta > 0:
            self.tem_canvas.yview("scroll", -3, "units")
        elif evt.delta < 0:
            self.tem_canvas.yview("scroll", 3, "units")


if __name__ == "__main__":
    main_window = MainWindow()
