from rubrica import Rubrica
from Consumatore import Consumatore
from Produttore import Produttore
import tkinter as tk
from tkinter import messagebox


class Finestra:

    def __init__(self, root):

        self.root = root
        self.root.title("Thread Manager")
        self.root.geometry("750x350")

        self.frame_title = tk.Frame(self.root, width=50, height=50, bg="black")
        self.frame_title.pack(fill=tk.BOTH, side=tk.TOP)

        self.main_title = tk.Label(self.frame_title, text="THREAD MANAGER", bg="black", fg="white",
                                   font=("Verdana", 30))
        self.main_title.pack(pady=10)

        self.frame1 = tk.Frame(master=self.root, width=200, height=200, bg="#17adb5", highlightbackground="black",
                               highlightthickness=8)
        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.frame2 = tk.Frame(master=self.root, width=200, height=200, bg="#b6e2d3", highlightbackground="black",
                               highlightthickness=8)
        self.frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.title1 = tk.Label(master=self.frame1, text="Simple Test", bg="#17adb5", fg="black", justify="center",
                               font=("Verdana", 20))
        self.title1.pack(pady=20)

        self.title2 = tk.Label(master=self.frame2, text="Multi-Thread Test", bg="#b6e2d3", fg="black",
                               font=("Verdana", 20))
        self.title2.pack(pady=20)

        self.description1 = tk.Label(master=self.frame1, text="Avvia una coppia\nproduttore-consumatore:", fg="black",
                                     bg="#17adb5", font=("Verdana", 14))
        self.description1.pack()

        self.description2 = tk.Label(master=self.frame2, text="Scegli il numero di coppie produttore-consumatore:",
                                     bg="#b6e2d3", fg="black", font=("Verdana", 14))
        self.description2.pack()

        self.btn1 = tk.Button(master=self.frame1, text="Avvia", activeforeground="#17adb5", height=2, width=10)
        self.btn1.pack(pady=20)
        self.btn1.bind("<Button-1>", self.handler_avvia1)

        self.entry = tk.Entry(master=self.frame2, width=10)
        self.entry.pack(pady=20)
        self.entry.focus()

        self.btn2 = tk.Button(master=self.frame2, text="Avvia", activeforeground="#b6e2d3", height=2, width=10)
        self.btn2.pack(pady=10)
        self.btn2.bind("<Button-1>", self.handler_avvia2)

        self.execution1 = tk.Label(master=self.frame1, text="", bg="#17adb5", font=("Verdana", 14))
        self.execution1.pack()
        self.msg1 = tk.StringVar()
        self.msg1.set("")
        self.execution1["textvariable"] = self.msg1

        self.execution2 = tk.Label(master=self.frame2, text="", bg="#b6e2d3", font=("Verdana", 14))
        self.execution2.pack(pady=10)
        self.msg2 = tk.StringVar()
        self.msg2.set("")
        self.execution2["textvariable"] = self.msg2

        self.root.mainloop()

    def handler_avvia1(self, event):
        self.msg1.set("Programma in esecuzione...")
        r = Rubrica()
        p = Produttore(r, 1)
        c = Consumatore(r, 1)
        p.start()
        c.start()
        p.join()
        c.join()
        self.msg1.set("Programma terminato.")

    def handler_avvia2(self, event):
        try:
            value = int(self.entry.get())
            self.msg2.set("Programma in esecuzione...")
            self.entry.delete(0, tk.END)
            r = Rubrica()
            threads = []
            for i in range(value):
                p = Produttore(r, i + 1)
                c = Consumatore(r, i + 1)
                threads.append(p)
                threads.append(c)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.msg2.set("Programma terminato.")
        except ValueError:
            messagebox.showerror(title="Ops!", message=f"Devi inserire un numero intero!")
            self.entry.delete(0, tk.END)
            self.entry.focus()


if __name__ == "__main__":
    window = Finestra(tk.Tk())
