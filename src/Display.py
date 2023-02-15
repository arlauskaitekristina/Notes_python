from tkinter import *
from tkinter import ttk
import src.Save_json


class Display:
    def __init__(self, f_display):
       columns = ("id", "name", "datetime")

       self.tree = ttk.Treeview(f_display, columns=columns, show="headings", selectmode="browse")
       self.tree.heading("id", text="№", command=lambda: self.sort(0, False))
       self.tree.heading("name", text="Имя пользователя", command=lambda: self.sort(1, False))
       self.tree.heading("datetime", text="Дата/Время", command=lambda: self.sort(2, False))
       
       self.tree.column("#1", stretch=NO, width=25)
       self.tree.column("#2", stretch=NO, width=240)
       self.tree.column("#3", stretch=NO, width=140)

       self.scrollbar = Scrollbar(f_display, orient=VERTICAL, command=self.tree.yview)
       self.tree.configure(yscrollcommand=self.scrollbar.set)
       self.tree.pack(side=LEFT)
       self.scrollbar.pack(side=RIGHT, fill=Y)

       self.update()

    def sort(self, col, reverse):
        l = sorted([(self.tree.set(k, col), k) for k in self.tree.get_children("")], reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort(col, not reverse))

    def update(self):
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        for item in self.tree.get_children():
            self.tree.delete(item)
        notes = src.Save_json.import_from_json()
        if notes is not None:
            for note in notes:
                self.tree.insert('', END,
                                 values=(note['id'], note['name'], note['datetime']))