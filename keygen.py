import random
import re
import tkinter as tk
from tkinter import ttk

class ProductKeyScheme:
    def generate(self):
        raise NotImplementedError
    def validate(self, key: str) -> bool:
        raise NotImplementedError

class Windows95OEM(ProductKeyScheme):
    def generate(self):
        day = f"{random.randint(1, 366):03}"
        year = f"{random.randint(4, 93):02}"
        middle = "OEM"
        while True:
            digits = [random.randint(0, 9) for _ in range(7)]
            if sum(digits) % 7 == 0:
                break
        z_part = ''.join(str(d) for d in digits)
        end = ''.join(str(random.randint(0, 9)) for _ in range(5))
        return f"{day}{year}-{middle}-0{z_part}-{end}"

    def validate(self, key: str) -> bool:
        match = re.match(r"^(\d{3})(\d{2})-OEM-0(\d{7})-(\d{5})$", key)
        if not match:
            return False
        day, year, z_part, _ = match.groups()
        if not (1 <= int(day) <= 366):
            return False
        if not (4 <= int(year) <= 93):
            return False
        if sum(int(d) for d in z_part) % 7 != 0:
            return False
        return True

class RetailSimple(ProductKeyScheme):
    def __init__(self, name):
        self.name = name

    def generate(self):
        while True:
            prefix = random.randint(0, 999)
            if prefix not in [333, 444, 555, 666, 777, 888, 999]:
                break
        while True:
            digits = [random.randint(0, 8) for _ in range(7)]
            if sum(digits) % 7 == 0:
                break
        suffix = ''.join(str(d) for d in digits)
        return f"{prefix:03}-{suffix}"

    def validate(self, key: str) -> bool:
        match = re.match(r"^(\d{3})-(\d{7})$", key)
        if not match:
            return False
        prefix, suffix = match.groups()
        if int(prefix) in [333, 444, 555, 666, 777, 888, 999]:
            return False
        if any(c not in '012345678' for c in suffix):
            return False
        if sum(int(c) for c in suffix) % 7 != 0:
            return False
        return True

class Windows98Retail(ProductKeyScheme):
    def generate(self):
        while True:
            prefix = random.randint(0, 999)
            if prefix not in [333, 444, 555, 666, 777, 888, 999]:
                break
        while True:
            digits = [random.randint(0, 9) for _ in range(7)]
            if sum(digits) % 7 == 0 and 1 <= digits[-1] <= 7:
                break
        suffix = ''.join(str(d) for d in digits)
        return f"{prefix:03}-{suffix}"

    def validate(self, key: str) -> bool:
        match = re.match(r"^(\d{3})-(\d{7})$", key)
        if not match:
            return False
        prefix, suffix = match.groups()
        if int(prefix) in [333, 444, 555, 666, 777, 888, 999]:
            return False
        if not suffix.isdigit():
            return False
        if sum(int(c) for c in suffix) % 7 != 0:
            return False
        if int(suffix[-1]) == 0 or int(suffix[-1]) >= 8:
            return False
        return True

class KeyManager:
    def __init__(self):
        self.schemes = {}

    def register_scheme(self, name: str, scheme: ProductKeyScheme):
        self.schemes[name] = scheme

    def generate(self, name: str) -> str:
        return self.schemes[name].generate()

    def validate(self, name: str, key: str) -> bool:
        return self.schemes[name].validate(key)

manager = KeyManager()
manager.register_scheme("Windows 95 OEM", Windows95OEM())
manager.register_scheme("Windows 98 OEM", Windows95OEM())  # same as 95 OEM
manager.register_scheme("Windows 95 Retail", RetailSimple("Windows 95 Retail"))
manager.register_scheme("Office 97 Retail", RetailSimple("Office 97 Retail"))
manager.register_scheme("Windows 98 Retail", Windows98Retail())

# GUI
def generate_key():
    product = product_var.get()
    key = manager.generate(product)
    output_var.set(f"Generated Key:\n{key}")

def validate_key():
    product = product_var.get()
    key = input_entry.get()
    valid = manager.validate(product, key)
    output_var.set("VALID" if valid else "INVALID")

root = tk.Tk()
root.title("Product Key Generator & Validator")

product_var = tk.StringVar(value="Windows 95 OEM")
output_var = tk.StringVar()

ttk.Label(root, text="Select Product:").pack(pady=5)
product_menu = ttk.Combobox(root, textvariable=product_var, values=list(manager.schemes.keys()), state="readonly")
product_menu.pack(pady=5)

ttk.Button(root, text="Generate Key", command=generate_key).pack(pady=5)

ttk.Label(root, text="Enter a Key to Validate:").pack(pady=5)
input_entry = ttk.Entry(root, width=40)
input_entry.pack(pady=5)

ttk.Button(root, text="Validate Key", command=validate_key).pack(pady=5)

output_label = ttk.Label(root, textvariable=output_var, foreground="blue", font=("Arial", 12), wraplength=400, justify="center")
output_label.pack(pady=10)

root.mainloop()
