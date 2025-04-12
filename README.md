# Warehouse Inventory & Order Management System

A desktop application built in Python that helps you manage warehouse inventory and customer orders with ease. The system features a polished GUI, persistent data storage using JSON, and the ability to export order logs to CSV files—all without any external dependencies.

---

## Table of Contents

- [Project Description](#project-description)
- [What the System Does](#what-the-system-does)
- [Who It’s For](#who-its-for)
- [Key Features](#key-features)
- [UI Overview](#ui-overview)
- [Tech Stack & Dependencies](#tech-stack--dependencies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation and Running Locally](#installation-and-running-locally)
  - [Directory Structure](#directory-structure)
- [Deployment](#deployment)
  - [Packaging as an Executable](#packaging-as-an-executable)
  - [Standalone Applications for Mac/Linux](#standalone-applications-for-maclinux)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Project Description

The **Warehouse Inventory & Order Management System** is a fully local, file-based desktop application designed for efficient warehouse operations. Built using Python 3 and Tkinter, the system provides robust functionality for managing inventory items and processing customer orders—all while ensuring that your data is safely persisted using JSON and easily exportable in CSV format.

---

## What the System Does

- **Inventory Management:**  
  Add, update, search for, and remove inventory items.
  
- **Order Processing:**  
  Handle customer orders using a FIFO (first-in, first-out) queue logic.
  
- **Persistent Storage:**  
  Automatically save changes to inventory and orders in JSON files. Auto-loads sample data if no saved data exists.
  
- **Data Export:**  
  Export fulfilled and unfulfilled order logs to CSV files.
  
- **Data Reset:**  
  Option to reset and clear all inventory and order data for a fresh start.

---

## Who It’s For

- **Small Businesses:**  
  Ideal for warehouses or small-medium enterprises looking for an affordable and reliable inventory solution.

- **Developers:**  
  A comprehensive example of integrating GUI, persistence, and data export in a local Python application.

- **Students:**  
  An excellent capstone project to learn Python desktop application development and practical software design.

---

## Key Features

- **Inventory Management:**
  - Add new items
  - Update stock quantities
  - Search for items by ID or name
  - Remove items from inventory

- **Order Processing:**
  - Submit new orders
  - Process orders using FIFO queue logic
  - Log fulfilled and unfulfilled orders

- **Data Persistence:**
  - Automatically save inventory and order data as JSON
  - Auto-load sample data when no data files exist

- **GUI with Tkinter:**
  - Polished, user-friendly interface
  - Resizable tables (Treeview) for live inventory updates
  - Status bar for real-time feedback
  - Grouped operations for clear user experience

- **Export & Reset:**
  - Export order logs to CSV
  - Reset all data (inventory and orders) with a single click

---

## UI Overview

The application has been designed with clarity and ease-of-use in mind:

- **Main Window:**  
  The primary interface displays the current inventory in a table that updates dynamically. Operations are logically grouped into panels for inventory and order management.

- **Dialogs & Popups:**  
  Input dialogs allow you to add or update items and orders. Popups provide confirmation and error messages for a seamless user experience.

- **Status Bar:**  
  A persistent status bar at the bottom of the window informs you of successful operations (e.g., "Item added", "Order processed").

---

## Tech Stack & Dependencies

- **Programming Language:** Python 3.x
- **GUI Library:** Tkinter (standard with Python)
- **Persistence:** JSON (using the built-in `json` module)
- **Export:** CSV (using the built-in `csv` module)
- **Other Modules:** `os` for file management

*No external libraries are required; everything is provided by Python’s standard library.*

---

## Getting Started

### Prerequisites

- **Python 3.x**: Download and install from [python.org](https://www.python.org/downloads/) if not already installed.
- **Tkinter**: Typically included with standard Python distributions. Verify installation using:
  ```bash
  python -m tkinter
  ```

### Installation and Running Locally

1. **Clone or Download the Repository:**

   ```bash
   git clone https://github.com/your_username/warehouse-inventory-order-management.git
   cd warehouse-inventory-order-management
   ```

2. **Run the Application:**

   Execute the GUI script using:
   ```bash
   python warehouse_gui.py
   ```
   The application will launch. If `inventory.json` and `orders.json` do not exist, sample data will be auto-loaded.

### Directory Structure

```
warehouse-inventory-order-management/
├── README.md
├── warehouse_backend.py      # Core classes: Item, InventoryManager, Order, OrderManager
├── warehouse_gui.py          # Tkinter GUI and persistence enhancements
├── inventory.json            # Auto-generated file for inventory data
├── orders.json               # Auto-generated file for order data
└── LICENSE                   # MIT License file
```

---

## Deployment

### Packaging as an Executable

To package the application as a standalone executable, use **PyInstaller**:

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Create an Executable:**

   ```bash
   pyinstaller --onefile warehouse_gui.py
   ```
   The executable will be available in the `dist` directory.

### Standalone Applications for Mac/Linux

For creating standalone applications on macOS or Linux, you can follow similar steps with PyInstaller. Alternatively, you may explore tools such as `cx_Freeze` for additional customization.

- **Optional:**  
  To add an icon or splash screen, include the `--icon` option with PyInstaller:
  ```bash
  pyinstaller --onefile --icon=app_icon.ico warehouse_gui.py
  ```

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the repository.**
2. **Create a feature branch:**  
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit your changes:**  
   Write descriptive commit messages.
4. **Submit a pull request** with details about your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

- Built with Python’s standard libraries – Tkinter, json, csv, and os.
- Special thanks to the open-source community for inspiring robust, secure, and user-friendly software solutions.

---

*This system is fully local, secure, and file-based. No internet connection or remote server is required for its operation.*
