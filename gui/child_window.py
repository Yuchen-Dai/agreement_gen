import tkinter


class ChildWindow:
    # count = 0

    @staticmethod
    def check():
        return True
        # return __class__.count == 0

    def __init__(self, master, width=1260, height=900, minsize_x=400, minsize_y=400, resizable=False, **data):
        if self.check():
            # __class__.count += 1
            self.window = tkinter.Toplevel(master=master)
            self.window.option_add("*Font", "黑体 15")
            self.window.title("合同生成器")
            self.window.resizable(width=resizable, height=resizable)
            self.window.geometry("%sx%s" % (width, height))
            self.window.minsize(minsize_x, minsize_y)
            self.window.configure(bg="#323232")
            self.window.update()
            self.window.protocol("WM_DELETE_WINDOW", self.close)
            self.data = data
            self.gui_init(self.window)
            self.window.mainloop()

    def close(self):
        # __class__.count -= 1
        self.window.destroy()

    def gui_init(self, window):
        pass