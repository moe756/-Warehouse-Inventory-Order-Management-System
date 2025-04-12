import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from warehouse_backend import InventoryManager, Item, Order, OrderManager
def item_to_dict(item):
    return {
        "item_id": item.item_id,
        "name": item.name,
        "quantity": item.quantity,
        "category": item.category
    }
def dict_to_item(d):
    return Item(d["item_id"], d["name"], d["quantity"], d.get("category", "General"))
def order_to_dict(order):
    return {
        "order_id": order.order_id,
        "items_ordered": order.items_ordered
    }
def dict_to_order(d):
    return Order(d["order_id"], d["items_ordered"])
def save_inventory_to_file(inventory_manager, filename="inventory.json"):
    data = [item_to_dict(item) for item in inventory_manager.items.values()]
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error saving inventory:", e)
def load_inventory_from_file(inventory_manager, filename="inventory.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            inventory_manager.items.clear()
            for item_data in data:
                item = dict_to_item(item_data)
                inventory_manager.items[item.item_id] = item
        except Exception as e:
            print("Error loading inventory:", e)
def save_orders_to_file(order_manager, filename="orders.json"):
    data = {
        "order_queue": [order_to_dict(order) for order in list(order_manager.order_queue)],
        "fulfilled_orders": [order_to_dict(order) for order in order_manager.fulfilled_orders],
        "unfulfilled_orders": [order_to_dict(order) for order in order_manager.unfulfilled_orders]
    }
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error saving orders:", e)
def load_orders_from_file(order_manager, filename="orders.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            order_manager.order_queue.clear()
            order_manager.fulfilled_orders.clear()
            order_manager.unfulfilled_orders.clear()
            for order_data in data.get("order_queue", []):
                order_manager.order_queue.append(dict_to_order(order_data))
            for order_data in data.get("fulfilled_orders", []):
                order_manager.fulfilled_orders.append(dict_to_order(order_data))
            for order_data in data.get("unfulfilled_orders", []):
                order_manager.unfulfilled_orders.append(dict_to_order(order_data))
        except Exception as e:
            print("Error loading orders:", e)
def launch_gui(inventory_manager, order_manager):
    load_inventory_from_file(inventory_manager)
    load_orders_from_file(order_manager)
    root = tk.Tk()
    root.title("Warehouse Inventory & Order Management System")
    root.geometry("900x650")
    default_font = ("Helvetica", 10)
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill="both", expand=True)
    frame_inventory = ttk.LabelFrame(main_frame, text="Inventory")
    frame_inventory.pack(fill="both", expand=True, padx=5, pady=5)
    tree = ttk.Treeview(frame_inventory, columns=("ID", "Name", "Category", "Quantity"), show="headings")
    tree.heading("ID", text="Item ID")
    tree.heading("Name", text="Name")
    tree.heading("Category", text="Category")
    tree.heading("Quantity", text="Quantity")
    tree.column("ID", anchor=tk.CENTER, width=80)
    tree.column("Name", anchor=tk.W, width=200)
    tree.column("Category", anchor=tk.CENTER, width=120)
    tree.column("Quantity", anchor=tk.CENTER, width=80)
    tree.pack(fill="both", expand=True, padx=5, pady=5)
    status_var = tk.StringVar()
    status_var.set("Ready")
    status_bar = ttk.Label(root, textvariable=status_var, relief="sunken", anchor=tk.W, padding=5, font=default_font)
    status_bar.pack(side="bottom", fill="x")
    def update_status(message):
        status_var.set(message)
    def refresh_inventory():
        for row in tree.get_children():
            tree.delete(row)
        for item in inventory_manager.items.values():
            tree.insert("", "end", values=(item.item_id, item.name, item.category, item.quantity))
        update_status("Inventory refreshed.")
    refresh_inventory()
    frame_item_ops = ttk.LabelFrame(main_frame, text="Item Operations", padding="10")
    frame_item_ops.pack(fill="x", padx=5, pady=5)
    frame_order_ops = ttk.LabelFrame(main_frame, text="Order Operations", padding="10")
    frame_order_ops.pack(fill="x", padx=5, pady=5)
    frame_misc_ops = ttk.LabelFrame(main_frame, text="Other Operations", padding="10")
    frame_misc_ops.pack(fill="x", padx=5, pady=5)
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
        save_inventory_to_file(inventory_manager)
        update_status(f"Item '{name}' added.")
    def update_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Update Item", "Please select an item to update.")
            return
        item_values = tree.item(selected[0])["values"]
        item_id = item_values[0]
        new_quantity = simpledialog.askinteger("Update Item", f"Enter new quantity for item {item_id}:", parent=root,
                                               minvalue=0)
        if new_quantity is None:
            return
        inventory_manager.update_item(item_id, new_quantity)
        refresh_inventory()
        save_inventory_to_file(inventory_manager)
        update_status(f"Item '{item_id}' updated.")
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
            save_inventory_to_file(inventory_manager)
            update_status(f"Item '{item_id}' removed.")
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
        update_status(f"Search completed for '{search_term}'.")
    def reset_inventory():
        if messagebox.askyesno("Reset Inventory", "This will clear all inventory and order data. Continue?"):
            inventory_manager.items.clear()
            order_manager.order_queue.clear()
            order_manager.fulfilled_orders.clear()
            order_manager.unfulfilled_orders.clear()
            refresh_inventory()
            save_inventory_to_file(inventory_manager)
            save_orders_to_file(order_manager)
            update_status("Inventory and order data reset.")
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
        save_orders_to_file(order_manager)
        update_status(f"Order '{order_id}' submitted.")
        messagebox.showinfo("Submit Order", f"Order {order_id} submitted successfully.")
    def process_next_order():
        order_manager.process_next_order()
        refresh_inventory()
        save_inventory_to_file(inventory_manager)
        save_orders_to_file(order_manager)
        update_status("Processed next order.")
        messagebox.showinfo("Process Order", "Processed next order.")
    def process_all_orders():
        order_manager.process_all_orders()
        refresh_inventory()
        save_inventory_to_file(inventory_manager)
        save_orders_to_file(order_manager)
        update_status("Processed all pending orders.")
        messagebox.showinfo("Process Orders", "Processed all pending orders.")
    def export_logs():
        order_manager.export_logs()
        update_status("Order logs exported.")
        messagebox.showinfo("Export Logs", "Order logs exported successfully.")
    ttk.Button(frame_item_ops, text="Add Item", command=add_item).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(frame_item_ops, text="Update Item", command=update_item).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(frame_item_ops, text="Remove Item", command=remove_item).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(frame_item_ops, text="Search Item", command=search_item).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(frame_item_ops, text="Reset Inventory", command=reset_inventory).grid(row=0, column=4, padx=5, pady=5)
    ttk.Button(frame_order_ops, text="Submit Order", command=submit_order).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(frame_order_ops, text="Process Next Order", command=process_next_order).grid(row=0, column=1, padx=5,                                                                                   pady=5)
    ttk.Button(frame_order_ops, text="Process All Orders", command=process_all_orders).grid(row=0, column=2, padx=5,                                                                                   pady=5)
    ttk.Button(frame_order_ops, text="Export Logs", command=export_logs).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(frame_misc_ops, text="Refresh Inventory", command=refresh_inventory).pack(padx=5, pady=5)
    root.mainloop()
if __name__ == "__main__":
    inventory_manager = InventoryManager()
    order_manager = OrderManager(inventory_manager)
    if not os.path.exists("inventory.json"):
        sample_items = [
            Item("A101", "Widget", 50, "Gadgets"),
            Item("B205", "Gizmo", 30, "Gadgets"),
            Item("C310", "Doodad", 20, "Accessories")
        ]
        for item in sample_items:
            inventory_manager.add_item(item)
        save_inventory_to_file(inventory_manager)
    launch_gui(inventory_manager, order_manager)
