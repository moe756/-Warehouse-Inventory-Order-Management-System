import sys
import csv
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
class Item:
    def __init__(self, item_id, name, quantity, category="General"):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.category = category
    def __str__(self):
        return f"[ID: {self.item_id}] {self.name} (Category: {self.category}, Qty: {self.quantity})"
class InventoryManager:
    def __init__(self):
        self.items = {}
    def add_item(self, item):
        if item.item_id in self.items:
            print("Item ID already exists. Consider updating the quantity instead.")
        else:
            self.items[item.item_id] = item
            print(f"Item '{item.name}' added successfully.")
    def update_item(self, item_id, quantity):
        if item_id in self.items:
            self.items[item_id].quantity = quantity
            print(f"Item '{self.items[item_id].name}' updated successfully.")
        else:
            print("Item not found in inventory.")
    def remove_item(self, item_id):
        if item_id in self.items:
            removed_item = self.items.pop(item_id)
            print(f"Item '{removed_item.name}' removed successfully.")
        else:
            print("Item not found in inventory.")
    def search_item(self, search_term):
        found = False
        for item in self.items.values():
            if search_term.lower() in item.item_id.lower() or search_term.lower() in item.name.lower():
                print(item)
                found = True
        if not found:
            print("No matching item found.")
    def display_inventory(self, sort_by="name"):
        if not self.items:
            print("Inventory is empty.")
            return
        try:
            sorted_items = sorted(self.items.values(), key=lambda x: getattr(x, sort_by))
        except AttributeError:
            print("Invalid sort key provided. Sorting by name instead.")
            sorted_items = sorted(self.items.values(), key=lambda x: x.name)
        print("\n--- Inventory List ---")
        for item in sorted_items:
            print(item)
        print("----------------------\n")
class Order:
    def __init__(self, order_id, items_ordered):
        self.order_id = order_id
        self.items_ordered = items_ordered  # e.g., {"item1": 3, "item2": 5}

    def __str__(self):
        items_str = ", ".join([f"{k}: {v}" for k, v in self.items_ordered.items()])
        return f"Order ID: {self.order_id} | Items: {items_str}"
class OrderManager:

    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager
        self.order_queue = deque()
        self.fulfilled_orders = []
        self.unfulfilled_orders = []

    def submit_order(self, order):
        self.order_queue.append(order)
        print(f"Order '{order.order_id}' submitted successfully.")

    def process_next_order(self):
        if not self.order_queue:
            print("No pending orders to process.")
            return
        order = self.order_queue.popleft()
        can_fulfill = True
        for item_id, qty in order.items_ordered.items():
            item = self.inventory_manager.items.get(item_id)
            if item is None:
                print(f"Item ID '{item_id}' does not exist in inventory for Order '{order.order_id}'.")
                can_fulfill = False
                break
            if item.quantity < qty:
                print(
                    f"Not enough stock for '{item.name}' (needed: {qty}, available: {item.quantity}) in Order '{order.order_id}'.")
                can_fulfill = False
                break
        if can_fulfill:
            for item_id, qty in order.items_ordered.items():
                self.inventory_manager.items[item_id].quantity -= qty
            self.fulfilled_orders.append(order)
            print(f"Order '{order.order_id}' has been fulfilled.")
        else:
            self.unfulfilled_orders.append(order)
            print(f"Order '{order.order_id}' could not be fulfilled due to inventory issues.")
    def process_all_orders(self):
        while self.order_queue:
            self.process_next_order()
    def export_logs(self):
        try:
            with open("fulfilled_orders.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Order ID", "Items Ordered"])
                for order in self.fulfilled_orders:
                    items_str = "; ".join([f"{k}:{v}" for k, v in order.items_ordered.items()])
                    writer.writerow([order.order_id, items_str])
            print("Fulfilled orders exported to fulfilled_orders.csv")
            with open("unfulfilled_orders.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Order ID", "Items Ordered"])
                for order in self.unfulfilled_orders:
                    items_str = "; ".join([f"{k}:{v}" for k, v in order.items_ordered.items()])
                    writer.writerow([order.order_id, items_str])
            print("Unfulfilled orders exported to unfulfilled_orders.csv")
        except Exception as e:
            print(f"Error exporting logs: {e}")
def display_menu():
    menu = """
--- Warehouse Management System ---
1. View Inventory
2. Add New Item
3. Update Existing Item Quantity
4. Remove Item
5. Search for an Item
6. Submit New Order
7. Process Next Order
8. Process All Orders
9. Export Order Logs to CSV
0. Exit
-------------------------------------
Choose an option: """
    return input(menu).strip()
def main():
    inventory_manager = InventoryManager()
    order_manager = OrderManager(inventory_manager)
    sample_items = [
        Item("A101", "Widget", 50, "Gadgets"),
        Item("B205", "Gizmo", 30, "Gadgets"),
        Item("C310", "Doodad", 20, "Accessories")
    ]
    for item in sample_items:
        inventory_manager.add_item(item)
    while True:
        choice = display_menu()

        if choice == "1":
            sort_by = input("Enter sort key (name/quantity/category) [default: name]: ").strip()
            if sort_by == "":
                sort_by = "name"
            inventory_manager.display_inventory(sort_by)

        elif choice == "2":
            item_id = input("Enter new item ID: ").strip()
            name = input("Enter item name: ").strip()
            try:
                quantity = int(input("Enter quantity: "))
            except ValueError:
                print("Invalid quantity. Must be an integer.")
                continue
            category = input("Enter item category [default: General]: ").strip()
            category = category if category else "General"
            new_item = Item(item_id, name, quantity, category)
            inventory_manager.add_item(new_item)

        elif choice == "3":
            item_id = input("Enter item ID to update: ").strip()
            try:
                quantity = int(input("Enter new quantity: "))
            except ValueError:
                print("Invalid quantity. Must be an integer.")
                continue
            inventory_manager.update_item(item_id, quantity)

        elif choice == "4":
            item_id = input("Enter item ID to remove: ").strip()
            inventory_manager.remove_item(item_id)

        elif choice == "5":
            search_term = input("Enter item ID or name to search: ").strip()
            inventory_manager.search_item(search_term)
        elif choice == "6":
            order_id = input("Enter order ID: ").strip()
            try:
                num_items = int(input("How many different items in the order? "))
            except ValueError:
                print("Invalid number. Must be an integer.")
                continue
            items_ordered = {}
            for _ in range(num_items):
                item_id = input("Enter item ID: ").strip()
                try:
                    qty = int(input("Enter quantity for this item: "))
                except ValueError:
                    print("Invalid quantity. Must be an integer.")
                    continue
                items_ordered[item_id] = qty
            new_order = Order(order_id, items_ordered)
            order_manager.submit_order(new_order)

        elif choice == "7":
            order_manager.process_next_order()

        elif choice == "8":
            order_manager.process_all_orders()

        elif choice == "9":
            order_manager.export_logs()

        elif choice == "0":
            print("Exiting the program.")
            sys.exit(0)

        else:
            print("Invalid option. Please choose a valid menu option.")


if __name__ == "__main__":
    pass

def launch_gui(inventory_manager, order_manager):
    root = tk.Tk()
    root.title("Warehouse Inventory & Order Fulfillment System")
    root.geometry("800x600")
    frame_inventory = ttk.LabelFrame(root, text="Inventory")
    frame_inventory.pack(fill="both", expand=True, padx=10, pady=10)
    tree = ttk.Treeview(frame_inventory, columns=("ID", "Name", "Category", "Quantity"), show="headings")
    tree.heading("ID", text="Item ID")
    tree.heading("Name", text="Name")
    tree.heading("Category", text="Category")
    tree.heading("Quantity", text="Quantity")
    tree.pack(fill="both", expand=True)
    def refresh_inventory():
        for row in tree.get_children():
            tree.delete(row)
        for item in inventory_manager.items.values():
            tree.insert("", "end", values=(item.item_id, item.name, item.category, item.quantity))

    refresh_inventory()
    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(fill="x", padx=10, pady=5)

    def add_item():
        item_id = simpledialog.askstring("Add Item", "Enter new Item ID:", parent=root)
        if not item_id:
            return
        name = simpledialog.askstring("Add Item", "Enter item name:", parent=root)
        if not name:
            return
        try:
            quantity = simpledialog.askinteger("Add Item", "Enter quantity:", parent=root, minvalue=0)
            if quantity is None:
                return
        except Exception:
            messagebox.showerror("Error", "Invalid quantity")
            return
        category = simpledialog.askstring("Add Item", "Enter item category (optional):", parent=root)
        if not category:
            category = "General"
        new_item = Item(item_id, name, quantity, category)
        inventory_manager.add_item(new_item)
        refresh_inventory()
    def update_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Update Item", "Select an item from the table to update.")
            return
        item_values = tree.item(selected[0])["values"]
        item_id = item_values[0]
        new_quantity = simpledialog.askinteger("Update Item", f"Enter new quantity for item {item_id}:", parent=root,
                                               minvalue=0)
        if new_quantity is None:
            return
        inventory_manager.update_item(item_id, new_quantity)
        refresh_inventory()
    def remove_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Remove Item", "Select an item to remove.")
            return
        item_values = tree.item(selected[0])["values"]
        item_id = item_values[0]
        if messagebox.askyesno("Remove Item", f"Are you sure you want to remove item {item_id}?"):
            inventory_manager.remove_item(item_id)
            refresh_inventory()
    def search_item():
        search_term = simpledialog.askstring("Search Item", "Enter Item ID or name to search:", parent=root)
        if not search_term:
            return
        matches = []
        for item in inventory_manager.items.values():
            if search_term.lower() in item.item_id.lower() or search_term.lower() in item.name.lower():
                matches.append(str(item))
        if matches:
            messagebox.showinfo("Search Results", "\n".join(matches))
        else:
            messagebox.showinfo("Search Results", "No matching items found.")
    def submit_order():
        order_id = simpledialog.askstring("Submit Order", "Enter Order ID:", parent=root)
        if not order_id:
            return
        try:
            num_items = simpledialog.askinteger("Submit Order", "How many different items in the order?", parent=root,
                                                minvalue=1)
            if num_items is None:
                return
        except Exception:
            messagebox.showerror("Error", "Invalid number")
            return
        items_ordered = {}
        for i in range(num_items):
            item_id = simpledialog.askstring("Order Item", f"Enter Item ID for item #{i + 1}:", parent=root)
            if not item_id:
                continue
            qty = simpledialog.askinteger("Order Item", f"Enter quantity for item {item_id}:", parent=root, minvalue=1)
            if qty is None:
                continue
            items_ordered[item_id] = qty
        if not items_ordered:
            messagebox.showwarning("Submit Order", "No valid items entered for the order.")
            return
        new_order = Order(order_id, items_ordered)
        order_manager.submit_order(new_order)
        messagebox.showinfo("Submit Order", f"Order {order_id} submitted successfully.")
    def process_next_order():
        order_manager.process_next_order()
        refresh_inventory()
        messagebox.showinfo("Process Order", "Processed next order.")
    def process_all_orders():
        order_manager.process_all_orders()
        refresh_inventory()
        messagebox.showinfo("Process Orders", "Processed all pending orders.")
    def export_logs():
        order_manager.export_logs()
        messagebox.showinfo("Export Logs", "Order logs exported successfully.")
    btn_add = ttk.Button(frame_buttons, text="Add Item", command=add_item)
    btn_update = ttk.Button(frame_buttons, text="Update Item", command=update_item)
    btn_remove = ttk.Button(frame_buttons, text="Remove Item", command=remove_item)
    btn_search = ttk.Button(frame_buttons, text="Search Item", command=search_item)
    btn_submit_order = ttk.Button(frame_buttons, text="Submit Order", command=submit_order)
    btn_process_next = ttk.Button(frame_buttons, text="Process Next Order", command=process_next_order)
    btn_process_all = ttk.Button(frame_buttons, text="Process All Orders", command=process_all_orders)
    btn_export = ttk.Button(frame_buttons, text="Export Logs", command=export_logs)
    btn_refresh = ttk.Button(frame_buttons, text="Refresh Inventory", command=refresh_inventory)
    btn_add.grid(row=0, column=0, padx=5, pady=5)
    btn_update.grid(row=0, column=1, padx=5, pady=5)
    btn_remove.grid(row=0, column=2, padx=5, pady=5)
    btn_search.grid(row=0, column=3, padx=5, pady=5)
    btn_submit_order.grid(row=1, column=0, padx=5, pady=5)
    btn_process_next.grid(row=1, column=1, padx=5, pady=5)
    btn_process_all.grid(row=1, column=2, padx=5, pady=5)
    btn_export.grid(row=1, column=3, padx=5, pady=5)
    btn_refresh.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
    root.mainloop()
if __name__ == "__main__":
    # Initialize backend objects with sample data.
    inventory_manager = InventoryManager()
    order_manager = OrderManager(inventory_manager)
    sample_items = [
        Item("A101", "Widget", 50, "Gadgets"),
        Item("B205", "Gizmo", 30, "Gadgets"),
        Item("C310", "Doodad", 20, "Accessories")
    ]
    for item in sample_items:
        inventory_manager.add_item(item)
    launch_gui(inventory_manager, order_manager)