import tkinter as tk
from tkinter import messagebox as mb
import requests
import matplotlib.pyplot as plt

def f_id(name):
    u = f"https://api.tvmaze.com/singlesearch/shows?q={name}"
    r = requests.get(u)
    if r.status_code != 200:
        return None
    return r.json()["id"]

def f_eps(i):
    u = f"https://api.tvmaze.com/shows/{i}/episodes"
    r = requests.get(u)
    if r.status_code != 200:
        return []
    return r.json()

def load():
    n = e.get().strip()
    if not n:
        mb.showerror("Input Error", "Enter show name.")
        return

    i = f_id(n)
    if not i:
        mb.showerror("Not Found", f"No show: {n}")
        return

    global s_d
    s_d = {}
    eps = f_eps(i)

    for ep in eps:
        s = ep["season"]
        num = ep["number"]
        r = ep["rating"]["average"]
        if r is not None:
            if s not in s_d:
                s_d[s] = []
            s_d[s].append((num, r))

    upd()

def upd():
    lst = sorted(s_d.keys())
    m = mnu["menu"]
    m.delete(0, "end")
    for s in lst:
        m.add_command(label=f"Season {s}", command=lambda v=s: sv.set(v))

def plt_r(*a):
    s = sv.get()
    if s not in s_d:
        return
    d = sorted(s_d[s])
    x = [i[0] for i in d]
    y = [i[1] for i in d]

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker='o', color='blue')
    plt.title(f"{e.get().strip().title()} - Season {s} Ratings")
    plt.xlabel("Ep")
    plt.ylabel("Rating")
    plt.ylim(0, 10)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

r = tk.Tk()
r.title("TV Ratings")

s_d = {}

tk.Label(r, text="Show:", font=("Arial", 12)).pack(pady=5)
e = tk.Entry(r, width=30, font=("Arial", 12))
e.pack(pady=5)

tk.Button(r, text="Load", command=load).pack(pady=5)

sv = tk.IntVar()
mnu = tk.OptionMenu(r, sv, ())
mnu.pack(pady=10)

sv.trace("w", plt_r)

r.mainloop()
