from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import src.Save_json


class Keys:
    def __init__(self, frame, display):
        self.display = display

        self.note_id_selected = None
        display.tree.bind("<<TreeviewSelect>>", lambda _: self.init_selection(display))

        self.new_key = ttk.Button(frame, text="Создать заметку", command=self.edit)
        self.new_key.pack()

        self.edit_key = ttk.Button(frame, text="Редактировать", state=DISABLED,
                                      command=lambda: self.edit(update=True))
        self.edit_key.pack()

        self.delete_key = ttk.Button(frame, text="Удалить", state=DISABLED,
                                        command=lambda: [
                                            src.Save_json.update_json(self.note_id_selected, delete=True),
                                            self.edit_key.configure(state=DISABLED),
                                            self.delete_key.configure(state=DISABLED),
                                            self.display.update()])
        self.delete_key.pack()

        self.update_key = ttk.Button(frame, text="Обновить", command=display.update)
        self.update_key.pack()

    def init_selection(self, display):
        if len(display.tree.selection()) > 0:
            self.note_id_selected = display.tree.item(display.tree.selection())['values'][0]
            self.edit_key['state'] = NORMAL
            self.delete_key['state'] = NORMAL
            print("Выбранный №:", self.note_id_selected)
        else:
            self.note_id_selected = None
            self.edit_key['state'] = DISABLED
            self.delete_key['state'] = DISABLED

    def edit(self, update=False):
        new_root = Tk()
        new_root.title("Новая запись")
        new_root.geometry("550x350")

        ttk.Label(new_root, text="Введите имя пользователя", padding=8).pack()

        entry = ttk.Entry(new_root)
        entry.pack()

        ttk.Label(new_root, text="Введите текст", padding=8).pack()

        word_editor = ScrolledText(new_root, width=22, height=12)
        word_editor.pack(anchor=N, fill=BOTH)

        save_key = ttk.Button(new_root, text="Сохранить", padding=8)
        if update:
            save_key.configure(
                command=lambda: [
                    src.Save_json.update_json(self.note_id_selected, entry.get(), word_editor.get("1.0", END)),
                    new_root.destroy(),
                    self.edit_key.configure(state=DISABLED),
                    self.delete_key.configure(state=DISABLED),
                    self.display.update()])
        else:
            save_key.configure(
                command=lambda: [src.Save_json.append_to_json(entry.get(), word_editor.get("1.0", END)),
                                 new_root.destroy(),
                                 self.edit_key.configure(state=DISABLED),
                                 self.delete_key.configure(state=DISABLED),
                                 self.display.update()])
        save_key.pack()

        if update:
            name, text = src.Save_json.update_json(self.note_id_selected, read=True)
            entry.insert(0, name)
            word_editor.insert(INSERT, text)
            word_editor.focus()

        new_root.mainloop()