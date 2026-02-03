import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length, use_lower, use_upper, use_digits, use_symbols):
    char_pools = []
    if use_lower:
        char_pools.append(string.ascii_lowercase)
    if use_upper:
        char_pools.append(string.ascii_uppercase)
    if use_digits:
        char_pools.append(string.digits)
    if use_symbols:
        char_pools.append(string.punctuation)

    if not char_pools:
        raise ValueError("At least one character type must be selected.")

    password_chars = [random.choice(pool) for pool in char_pools]

    all_chars = ''.join(char_pools)
    remaining_length = length - len(password_chars)
    if remaining_length < 0:
        raise ValueError(
            "Password length must be at least equal to the number "
            "of selected character types."
        )

    password_chars += [random.choice(all_chars) for _ in range(remaining_length)]
    random.shuffle(password_chars)
    return ''.join(password_chars)

def on_generate():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError("Length must be positive.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive integer for length.")
        return

    use_lower = var_lower.get() == 1
    use_upper = var_upper.get() == 1
    use_digits = var_digits.get() == 1
    use_symbols = var_symbols.get() == 1

    try:
        pwd = generate_password(length, use_lower, use_upper, use_digits, use_symbols)
        result_var.set(pwd)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def on_copy():
    pwd = result_var.get()
    if not pwd:
        messagebox.showinfo("Copy", "No password to copy.")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copy", "Password copied to clipboard.")

# GUI setup
root = tk.Tk()
root.title("Password Generator")
root.resizable(False, False)

# Length
length_frame = tk.Frame(root)
length_frame.pack(padx=10, pady=5, fill="x")
tk.Label(length_frame, text="Password length:").pack(side="left")
length_entry = tk.Entry(length_frame, width=10)
length_entry.pack(side="left", padx=5)
length_entry.insert(0, "12")

# Options
options_frame = tk.LabelFrame(root, text="Character options")
options_frame.pack(padx=10, pady=5, fill="x")

var_lower = tk.IntVar(value=1)
var_upper = tk.IntVar(value=1)
var_digits = tk.IntVar(value=1)
var_symbols = tk.IntVar(value=1)

tk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=var_lower).pack(anchor="w")
tk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=var_upper).pack(anchor="w")
tk.Checkbutton(options_frame, text="Digits (0-9)", variable=var_digits).pack(anchor="w")
tk.Checkbutton(options_frame, text="Symbols (!, @, #, ...)", variable=var_symbols).pack(anchor="w")

# Generate button
btn_frame = tk.Frame(root)
btn_frame.pack(padx=10, pady=5, fill="x")
tk.Button(btn_frame, text="Generate Password", command=on_generate).pack(side="left")

# Result
result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=5, fill="x")
tk.Label(result_frame, text="Generated password:").pack(anchor="w")
result_var = tk.StringVar()
result_entry = tk.Entry(result_frame, textvariable=result_var, width=40)
result_entry.pack(side="left", padx=(0,5))
tk.Button(result_frame, text="Copy", command=on_copy).pack(side="left")

root.mainloop()