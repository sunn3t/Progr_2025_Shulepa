import tkinter as tk

def check_palindrome():
    text = entry_str.get()
    if text == text[::-1]:
        label_result.config(text="Це паліндром.")
    else:
        label_result.config(text="Це не паліндром.")


root = tk.Tk()
root.title("T24.2: Перевірка паліндрома")
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Рядок:").grid(row=0, column=0, padx=5, pady=5)
entry_str = tk.Entry(frame_input, width=30)
entry_str.grid(row=0, column=1, padx=5, pady=5)

btn_check = tk.Button(root, text="Перевірити", command=check_palindrome)
btn_check.pack(pady=5)

label_result = tk.Label(root, text="")
label_result.pack(pady=5)
root.mainloop()
