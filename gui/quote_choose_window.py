import tkinter
import tkinter.ttk
from child_window import ChildWindow


class QuoteChooseWindow(ChildWindow):
    def __init__(self, master, command):
        self.command = command
        super().__init__(master, 500, 800, 500, 800, False)

    def gui_init(self, window):
        button_disabled_img = tkinter.PhotoImage(file="img/button_disabled.png", width=110, height=50)
        button_enabled_img = tkinter.PhotoImage(file="img/button_enabled.png", width=110, height=50)
        confirm_button = tkinter.Label(window, width=110, height=50, image=button_disabled_img, text="确定",
                                       bg="#323232", fg="#E4E4E4", compound="center", cursor="arrow")
        confirm_button.pack(side="bottom")
        self.data["button_enabled_img"] = button_enabled_img
        self.data["button_disabled_img"] = button_disabled_img

        tkinter.Frame(window, bg="#323232", height=10).pack(side="bottom", fill="x")

        quote_tree_view = tkinter.ttk.Treeview(window, show="tree", style="Custom.Treeview")

        quote_tree_scroll = tkinter.Scrollbar(quote_tree_view, command=quote_tree_view.yview)
        quote_tree_view.configure(yscrollcommand=quote_tree_scroll.set)

        quote_tree_scroll.pack(side="right", fill="y")
        quote_tree_view.pack(side="top", expand=1, fill="both")

        no_choice = quote_tree_view.insert("", 0, "no_choice", text="不选择报价单", values=("noChoice",))
        test_year01 = quote_tree_view.insert("", 1, "year01", text="2020", values=("2020",))
        test_month01 = quote_tree_view.insert(test_year01, 0, "month01", text="01", values=("2020", "01"))
        test_month02 = quote_tree_view.insert(test_year01, 1, "month02", text="02", values=("2020", "02"))
        test_file01 = quote_tree_view.insert(test_month01, 0, "file01", text="测试数据01", values=("2020", "01", "001"))
        test_file02 = quote_tree_view.insert(test_month01, 1, "file02", text="测试数据02", values=("2020", "01", "002"))
        test_file03 = quote_tree_view.insert(test_month02, 0, "file03", text="测试数据03", values=("2020", "02", "003"))

        collect_img = tkinter.PhotoImage(file="img/tv_chosen.png", width=15, height=15)
        self.data["collect_img"] = collect_img

        def get_confirm(qid):
            def confirm(evt):
                self.close()
                self.command(qid)
            return confirm

        self.data["last_selection"] = None

        def quote_select(evt):
            tree_view = evt.widget
            selection = tree_view.selection()

            if self.data["last_selection"] is not None:
                tree_view.item(self.data["last_selection"], image="")

            tree_view.item(selection[0], image=collect_img)
            self.data["last_selection"] = selection[0]

            choice = tree_view.item(selection[0], "values")
            if len(choice) < 3 and choice[0] != "noChoice":
                confirm_button.config(image=button_disabled_img, cursor="arrow")
                confirm_button.unbind("<Button-1>")
            else:
                confirm_button.config(image=button_enabled_img, cursor="hand2")
                confirm_button.unbind("<Button-1>")
                qid = choice[0] if len(choice) < 3 else choice[2]
                confirm_button.bind("<Button-1>", get_confirm(qid))

        quote_tree_view.bind('<<TreeviewSelect>>', quote_select)

