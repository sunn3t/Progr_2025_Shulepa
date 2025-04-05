import tkinter as tk
from tkinter import messagebox

sign_changes = 0
last_sign = None

def process_number():
    global sign_changes, last_sign
    try:
        num = int(entry_num.get())
    except ValueError:
        messagebox.showerror("Помилка", "Невірний формат цілого числа.")
        return

    entry_num.delete(0, tk.END)

    if num == 0:
        label_result.config(text=f"Кількість змін знаку: {sign_changes}")
        # За бажання можна відключити кнопку або завершити обробку
        # btn_process.config(state=tk.DISABLED)
        return

    current_sign = 1 if num > 0 else -1

    if last_sign is not None and current_sign != last_sign:
        sign_changes += 1
    last_sign = current_sign
    label_result.config(text=f"Поточна кількість змін знаку: {sign_changes}")


root = tk.Tk()
root.title("T24.4: Підрахунок змін знаку в послідовності")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Введіть число (0 – завершити):").grid(row=0, column=0, padx=5, pady=5)
entry_num = tk.Entry(frame_input, width=10)
entry_num.grid(row=0, column=1, padx=5, pady=5)

btn_process = tk.Button(root, text="Обробити", command=process_number)
btn_process.pack(pady=5)
label_result = tk.Label(root, text="Поточна кількість змін знаку: 0")
label_result.pack(pady=5)

root.mainloop()
