import tkinter as tk
from tkinter import ttk, messagebox


class BreakfastOrderSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eggcellent Eats Order System")
        self.geometry("800x600")
        self.order_items = []
        
        # Create main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)


        # Menu Categories
        self.create_menu_buttons()
        self.create_order_summary()
        self.create_checkout_section()


    def create_menu_buttons(self):
        """Create menu category selection buttons"""
        menu_frame = ttk.LabelFrame(self.main_frame, text="Menu Categories")
        menu_frame.pack(pady=10, fill=tk.X)
        
        categories = ["Breakfast Plates", "Beverages", "Sides"]
        for idx, category in enumerate(categories):
            btn = ttk.Button(menu_frame, text=category, 
                            command=lambda c=category: self.show_menu_items(c))
            btn.grid(row=0, column=idx, padx=5, pady=5)


    def show_menu_items(self, category):
        """Display items for selected category"""
        items = {
            "Breakfast Plates": [
                ("Pancakes", 8.99),
                ("Omelette", 9.50),
                ("French Toast", 7.95)
            ],
            "Beverages": [
                ("Coffee", 2.50),
                ("Orange Juice", 3.00),
                ("Smoothie", 4.50)
            ],
            "Sides": [
                ("Bacon", 3.00),
                ("Hash Browns", 2.50),
                ("Fruit Cup", 4.00)
            ]
        }
        
        # Clear previous items
        if hasattr(self, 'items_frame'):
            self.items_frame.destroy()
            
        self.items_frame = ttk.LabelFrame(self.main_frame, text=category)
        self.items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for row, (item, price) in enumerate(items[category]):
            item_frame = ttk.Frame(self.items_frame)
            item_frame.grid(row=row, column=0, sticky="w", padx=5, pady=2)
            
            ttk.Label(item_frame, text=f"{item} - ${price:.2f}").pack(side=tk.LEFT)
            ttk.Button(item_frame, text="Customize & Add", 
                      command=lambda i=item, p=price: self.customize_item(i, p)
                     ).pack(side=tk.RIGHT, padx=5)


    def customize_item(self, item, price):
        """Open customization window"""
        customize_win = tk.Toplevel(self)
        customize_win.title(f"Customize {item}")
        
        # Quantity selection
        ttk.Label(customize_win, text="Quantity:").grid(row=0, column=0)
        quantity = tk.Spinbox(customize_win, from_=1, to=10, width=5)
        quantity.grid(row=0, column=1)
        quantity.delete(0, "end")
        quantity.insert(0, "1")
        
        # Toppings/options
        options_frame = ttk.LabelFrame(customize_win, text="Options")
        options_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        options = {
            "Pancakes": ["Syrup", "Whipped Cream", "Fruit"],
            "Omelette": ["Cheese", "Mushrooms", "Ham"],
            "Coffee": ["Milk", "Sugar", "Vanilla"]
        }.get(item, [])
        
        selected_options = []
        for idx, opt in enumerate(options):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(options_frame, text=opt, variable=var)
            cb.grid(row=idx//2, column=idx%2, sticky="w")
            selected_options.append((opt, var))
        
        # Add to order button
        ttk.Button(customize_win, text="Add to Order", 
                  command=lambda: self.add_to_order(
                      item, price, int(quantity.get()), 
                      [opt for opt, var in selected_options if var.get()]
                  )).grid(row=2, columnspan=2, pady=10)


    def add_to_order(self, item, price, quantity, options):
        """Add customized item to order"""
        self.order_items.append({
            "item": item,
            "price": price,
            "quantity": quantity,
            "options": options
        })
        self.update_order_summary()


    def update_order_summary(self):
        """Refresh order summary display"""
        self.order_list.delete(*self.order_list.get_children())
        total = 0
        
        for item in self.order_items:
            options = ", ".join(item["options"]) if item["options"] else "None"
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            
            self.order_list.insert("", "end", values=(
                f"{item['quantity']}x {item['item']}",
                options,
                f"${subtotal:.2f}"
            ))
        
        tax = total * 0.08
        self.total_var.set(f"Total: ${total + tax:.2f} (incl. 8% tax)")


    def create_order_summary(self):
        """Create order summary treeview"""
        summary_frame = ttk.LabelFrame(self.main_frame, text="Order Summary")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Item", "Options", "Price")
        self.order_list = ttk.Treeview(summary_frame, columns=columns, show="headings")
        
        for col in columns:
            self.order_list.heading(col, text=col)
            self.order_list.column(col, width=200)
        
        self.order_list.pack(fill=tk.BOTH, expand=True)
        
        self.total_var = tk.StringVar()
        ttk.Label(summary_frame, textvariable=self.total_var).pack(pady=5)


    def create_checkout_section(self):
        """Create payment and checkout controls"""
        checkout_frame = ttk.Frame(self.main_frame)
        checkout_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.payment_var = tk.StringVar(value="Cash")
        ttk.Radiobutton(checkout_frame, text="Cash", 
                       variable=self.payment_var, value="Cash").pack(side=tk.LEFT)
        ttk.Radiobutton(checkout_frame, text="Card", 
                       variable=self.payment_var, value="Card").pack(side=tk.LEFT)
        
        ttk.Button(checkout_frame, text="Place Order", 
                  command=self.place_order).pack(side=tk.RIGHT)


    def place_order(self):
        """Handle order finalization"""
        if not self.order_items:
            messagebox.showerror("Error", "Please add items to your order first!")
            return
        
        receipt = "=== Eggcellent Eats Receipt ===\n"
        for item in self.order_items:
            receipt += f"{item['quantity']}x {item['item']} ({', '.join(item['options'])}) - ${item['price'] * item['quantity']:.2f}\n"
        
        total = sum(item["price"] * item["quantity"] for item in self.order_items)
        tax = total * 0.08
        receipt += f"\nSubtotal: ${total:.2f}\n"
        receipt += f"Tax (7%): ${tax:.2f}\n"
        receipt += f"Total: ${total + tax:.2f}\n"
        receipt += f"Payment Method: {self.payment_var.get()}\n"
        receipt += "Thank you for your order!"
        
        messagebox.showinfo("Order Confirmed", receipt)
        self.order_items.clear()
        self.update_order_summary()


if __name__ == "__main__":
    app = BreakfastOrderSystem()
    app.mainloop()
