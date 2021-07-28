import tkinter


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

    def delete_all(self):
        self.items = list()
        self.draw()

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


class CustomText(tkinter.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tkinter.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result
