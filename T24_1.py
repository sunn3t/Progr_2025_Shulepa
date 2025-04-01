import tkinter as tk
from tkinter import messagebox

def calculate_series():
    try:
        x = float(entry_x.get())
        eps = float(entry_eps.get())
    except ValueError:
        messagebox.showerror("Помилка", "Невірний формат чисел.")
        return

    if abs(x) >= 1:
        messagebox.showerror("Помилка", "Необхідно, щоб |x| < 1.")
        return
    
    n = 0
    term = 1.0
    s = 0.0
    
    while abs(term) >= eps:
        s += term
        n += 1
        term = (n + 1) * ((-1)**n) * (x**n)
    
    label_result.config(text=f"Сума: {s:.6f}")


root = tk.Tk()
root.title("T24.1: Сума ряду")


frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="x:").grid(row=0, column=0, padx=5, pady=5)
entry_x = tk.Entry(frame_input, width=10)
entry_x.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="ε:").grid(row=1, column=0, padx=5, pady=5)
entry_eps = tk.Entry(frame_input, width=10)
entry_eps.grid(row=1, column=1, padx=5, pady=5)

btn_calculate = tk.Button(root, text="Обчислити", command=calculate_series)
btn_calculate.pack(pady=5)

label_result = tk.Label(root, text="Сума: ")
label_result.pack(pady=5)
root.mainloop()
