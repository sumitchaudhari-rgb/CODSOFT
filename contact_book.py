import tkinter as tk
from tkinter import ttk, messagebox


class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        # Make window full size (maximized)
        try:
            self.root.state("zoomed")   # Windows
        except tk.TclError:
            self.root.attributes("-zoomed", True)  # Some other platforms

        # Light theme colors
        self.bg_color = "#f5f5f5"
        self.card_color = "#ffffff"
        self.accent_color = "#1976d2"
        self.text_color = "#333333"
        self.border_color = "#d0d0d0"

        self.root.configure(bg=self.bg_color)

        # In-memory contact list: each is a dict
        self.contacts = []  # {id, name, phone, email, address}
        self.next_id = 1

        self.build_ui()

    def build_ui(self):
        # Top title bar
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        title_label = tk.Label(
            title_frame,
            text="Contact Manager",
            font=("Segoe UI", 22, "bold"),
            fg=self.accent_color,
            bg=self.bg_color,
        )
        title_label.pack(side="left", padx=(10, 0))

        # Main container
        main_frame = tk.Frame(
            self.root,
            bg=self.card_color,
            bd=1,
            relief="solid",
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: Form
        form_frame = tk.Frame(main_frame, bg=self.card_color)
        form_frame.pack(side="left", fill="y", padx=20, pady=20)

        form_title = tk.Label(
            form_frame,
            text="Contact Details",
            font=("Segoe UI", 14, "bold"),
            fg=self.text_color,
            bg=self.card_color,
        )
        form_title.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Name
        tk.Label(
            form_frame,
            text="Name:",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color,
        ).grid(row=1, column=0, sticky="e", pady=5, padx=(0, 5))
        self.name_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 10))
        self.name_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Phone
        tk.Label(
           form_frame,
            text="Phone:",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color,
        ).grid(row=2, column=0, sticky="e", pady=5, padx=(0, 5))
        self.phone_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 10))
        self.phone_entry.grid(row=2, column=1, sticky="w", pady=5)

        # Email
        tk.Label(
            form_frame,
            text="Email:",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color,
        ).grid(row=3, column=0, sticky="e", pady=5, padx=(0, 5))
        self.email_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 10))
        self.email_entry.grid(row=3, column=1, sticky="w", pady=5)

        # Address (multi-line)
        tk.Label(
            form_frame,
            text="Address:",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color,
        ).grid(row=4, column=0, sticky="ne", pady=5, padx=(0, 5))
        self.address_text = tk.Text(form_frame, width=30, height=4, font=("Segoe UI", 10))
        self.address_text.grid(row=4, column=1, sticky="w", pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.card_color)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0))

        self.add_button = tk.Button(
            btn_frame,
            text="Add Contact",
            font=("Segoe UI", 10, "bold"),
            bg="#4caf50",
            fg="white",
            activebackground="#43a047",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.add_contact,
        )
        self.add_button.pack(side="left", padx=5)

        self.update_button = tk.Button(
            btn_frame,
            text="Update Contact",
            font=("Segoe UI", 10, "bold"),
            bg="#1976d2",
            fg="white",
            activebackground="#1565c0",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.update_contact,
        )
        self.update_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(
            btn_frame,
            text="Delete Contact",
            font=("Segoe UI", 10, "bold"),
            bg="#e53935",
            fg="white",
            activebackground="#c62828",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.delete_contact,
        )
        self.delete_button.pack(side="left", padx=5)

        self.clear_button = tk.Button(
            btn_frame,
            text="Clear Form",
            font=("Segoe UI", 10, "bold"),
            bg="#9e9e9e",
            fg="white",
            activebackground="#757575",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.clear_form,
        )
        self.clear_button.pack(side="left", padx=5)

        # Right: Search + List
        right_frame = tk.Frame(main_frame, bg=self.card_color)
        right_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Search bar
        search_frame = tk.Frame(right_frame, bg=self.card_color)
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            search_frame,
            text="Search (Name or Phone):",
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.card_color,
        ).pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30,
            font=("Segoe UI", 10),
        )
        self.search_entry.pack(side="left", padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_contact_list())

        self.clear_search_button = tk.Button(
            search_frame,
            text="Clear",
            font=("Segoe UI", 9),
            bg="#eeeeee",
            fg="#333333",
            activebackground="#e0e0e0",
            activeforeground="#333333",
            relief="flat",
            command=self.clear_search,
        )
        self.clear_search_button.pack(side="left", padx=(5, 0))

        # Treeview (contact list)
        list_frame = tk.Frame(right_frame, bg=self.card_color)
        list_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "name", "phone", "email", "address"),
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("email", text="Email")
        self.tree.heading("address", text="Address")

        self.tree.column("id", width=0, stretch=False, anchor="w")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("phone", width=120, anchor="w")
        self.tree.column("email", width=180, anchor="w")
        self.tree.column("address", width=250, anchor="w")

        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Style Treeview for light mode
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="white",
            foreground=self.text_color,
            rowheight=22,
            fieldbackground="white",
            bordercolor=self.border_color,
            borderwidth=1,
        )
        style.configure(
            "Treeview.Heading",
            background="#e0e0e0",
            foreground="#333333",
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", "#bbdefb")],
            foreground=[("selected", "#000000")],
        )

        self.refresh_contact_list()

    # ---- Helpers ----
    def get_form_data(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", "end").strip()
        return name, phone, email, address

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.address_text.delete("1.0", "end")
        self.tree.selection_remove(self.tree.selection())

    def clear_search(self):
        self.search_var.set("")
        self.refresh_contact_list()

    # ---- CRUD operations ----
    def add_contact(self):
        name, phone, email, address = self.get_form_data()

        if not name or not phone:
            messagebox.showwarning("Missing Data", "Name and Phone are required.")
            return

        contact = {
            "id": self.next_id,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
        }
        self.next_id += 1
        self.contacts.append(contact)

        self.refresh_contact_list()
        self.clear_form()
        messagebox.showinfo("Success", "Contact added successfully.")

    def update_contact(self):
        selected_id = self.get_selected_contact_id()
        if selected_id is None:
            messagebox.showwarning("No Selection", "Please select a contact to update.")
            return

        name, phone, email, address = self.get_form_data()
        if not name or not phone:
            messagebox.showwarning("Missing Data", "Name and Phone are required.")
            return

        for contact in self.contacts:
            if contact["id"] == selected_id:
                contact["name"] = name
                contact["phone"] = phone
                contact["email"] = email
                contact["address"] = address
                break

        self.refresh_contact_list()
        messagebox.showinfo("Success", "Contact updated successfully.")

    def delete_contact(self):
        selected_id = self.get_selected_contact_id()
        if selected_id is None:
            messagebox.showwarning("No Selection", "Please select a contact to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if not confirm:
            return

        self.contacts = [c for c in self.contacts if c["id"] != selected_id]
        self.refresh_contact_list()
        self.clear_form()
        messagebox.showinfo("Deleted", "Contact deleted successfully.")

    def refresh_contact_list(self):
        search_text = self.search_var.get().strip().lower()

        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert filtered contacts
        for contact in self.contacts:
            if search_text:
                if (search_text not in contact["name"].lower()
                        and search_text not in contact["phone"].lower()):
                    continue

            self.tree.insert(
                "",
                "end",
                values=(
                    contact["id"],
                    contact["name"],
                    contact["phone"],
                    contact["email"],
                    contact["address"].replace("\n", " "),
                ),
            )

    def on_tree_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item = selection[0]
        values = self.tree.item(item, "values")
        # values: (id, name, phone, email, address)
        _, name, phone, email, address = values

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, name)

        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, phone)

        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, email)

        self.address_text.delete("1.0", "end")
        self.address_text.insert("1.0", address)

    # Helper to get ID from first value
    def get_selected_contact_id(self):
        selection = self.tree.selection()
        if not selection:
            return None
        item_id = selection[0]
        values = self.tree.item(item_id, "values")
        if not values:
            return None
        return int(values[0])


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()