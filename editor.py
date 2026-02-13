import os, json
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "slots.json"

class PromptEditor:
    def __init__(self, win):
        self.win = win
        self.win.title("Prompt Manager")
        self.win.geometry("600x620")
        
        os.chdir(os.path.dirname(__file__))
        
        self.data = self.load()
        self.is_rec = False 
        
        self.init_ui()
        self.load_list()

    def load(self):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"slots": []}

    def save(self):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def init_ui(self):

        frame_top = tk.Frame(self.win)
        frame_top.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(frame_top, columns=("id", "key", "file"), show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("key", text="Hotkey")
        self.tree.heading("file", text="File Name")
        self.tree.column("id", width=40)
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.show_detail)

        f_key = tk.LabelFrame(self.win, text=" Keybind ")
        f_key.pack(fill="x", padx=10, pady=5)
        
        self.lbl_key = tk.Label(f_key, text="Key: None", fg="blue")
        self.lbl_key.pack(side="left", padx=5, pady=5)
        
        self.btn_rec = tk.Button(f_key, text="Set Hotkey", command=self.start_rec)
        self.btn_rec.pack(side="right", padx=5, pady=5)

        f_edit = tk.LabelFrame(self.win, text=" Prompt Content ")
        f_edit.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt = tk.Text(f_edit, height=12, font=("Courier New", 10))
        self.txt.pack(fill="both", expand=True, padx=5, pady=5)

        f_btns = tk.Frame(self.win)
        f_btns.pack(pady=10)
        
        tk.Button(f_btns, text="Add", width=10, command=self.add_item).pack(side="left", padx=5)
        tk.Button(f_btns, text="Save", width=10, command=self.do_save).pack(side="left", padx=5)
        tk.Button(f_btns, text="Delete", width=10, command=self.do_del).pack(side="left", padx=5)

        self.win.bind("<Key>", self.on_key)

    def load_list(self):
        self.tree.delete(*self.tree.get_children())
        for s in self.data["slots"]:
            self.tree.insert("", "end", values=(s["id"], s["hotkey"], s["file"]))

    def show_detail(self, _):
        sel = self.tree.selection()
        if not sel: return
        sid = self.tree.item(sel[0])['values'][0]
        
        for s in self.data["slots"]:
            if s["id"] == sid:
                self.txt.delete("1.0", tk.END)
                self.txt.insert("1.0", s["content"])
                self.lbl_key.config(text=f"Key: {s['hotkey']}")

    def start_rec(self):
        if not self.tree.selection(): return
        self.is_rec = True
        self.btn_rec.config(text="LISTENING...", relief="sunken")

    def on_key(self, e):
        if not self.is_rec: return
        if e.keysym in ("Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R"): return

        if e.keysym == "Escape":
            self.is_rec = False
            self.btn_rec.config(text="Set Hotkey", relief="raised")
            return

        mods = []
        if e.state & 0x4: mods.append("Ctrl")
        if e.state & 0x1: mods.append("Shift")
        
        key = e.char.upper() if e.char.isalnum() else e.keysym.capitalize()
        new_bind = "+".join(mods + [key])

        sid = self.tree.item(self.tree.selection()[0])['values'][0]
        for s in self.data["slots"]:
            if s["id"] == sid:
                s["hotkey"] = new_bind
                break
        
        self.save()
        self.load_list()
        self.is_rec = False
        self.btn_rec.config(text="Set Hotkey", relief="raised")
        self.lbl_key.config(text=f"Key: {new_bind}")

    def add_item(self):
        if len(self.data["slots"]) >= 10: return
        
        ids = [s["id"] for s in self.data["slots"]]
        new_id = 1
        while new_id in ids: new_id += 1
            
        self.data["slots"].append({
            "id": new_id,
            "hotkey": f"F{new_id}",
            "file": f"Prompt_{new_id}.txt",
            "content": ""
        })
        self.save()
        self.load_list()

    def do_save(self):
        sel = self.tree.selection()
        if not sel: return
        sid = self.tree.item(sel[0])['values'][0]
        val = self.txt.get("1.0", "end-1c").strip()
        
        for s in self.data["slots"]:
            if s["id"] == sid:
                s["content"] = val
                break
        self.save()
        messagebox.showinfo("Done", "Saved!")

    def do_del(self):
        sel = self.tree.selection()
        if not sel or not messagebox.askyesno("?", "Delete?"): return
        sid = self.tree.item(sel[0])['values'][0]
        self.data["slots"] = [s for s in self.data["slots"] if s["id"] != sid]
        self.save()
        self.load_list()
        self.txt.delete("1.0", tk.END)

if __name__ == "__main__":
    app = tk.Tk()
    PromptEditor(app)
    app.mainloop()