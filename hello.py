import csv
import os

FILENAME = "medicines.csv"

def initialize_file():
    
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Quantity", "Price"])

def load_medicines():
    """Loads medicines from medicines.csv into a list of dictionaries."""
    initialize_file()
    medicines = []
    with open(FILENAME, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            medicines.append({
                "ID": row["ID"],
                "Name": row["Name"],
                "Quantity": int(row["Quantity"]),
                "Price": float(row["Price"])
            })
    return medicines

def save_medicines(medicines):
    
    with open(FILENAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Quantity", "Price"])
        for med in medicines:
            writer.writerow([med["ID"], med["Name"], med["Quantity"], med["Price"]])

def generate_next_id(medicines):
    
    if not medicines:
        return "M1"
    # Extract numeric part from IDs like 'M1', 'M2', etc.
    max_id = 0
    for med in medicines:
        try:
            num = int(med["ID"][1:])
            if num > max_id:
                max_id = num
        except ValueError:
            continue
    return f"M{max_id + 1}"

def add_medicine(medicines):
    
    name = input("Name: ").strip()
    try:
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
        
        if quantity < 0 or price < 0:
            print("Error: Quantity and Price cannot be negative.")
            return
            
        med_id = generate_next_id(medicines)
        new_med = {
            "ID": med_id,
            "Name": name,
            "Quantity": quantity,
            "Price": price
        }
        medicines.append(new_med)
        save_medicines(medicines)
        print(f"Medicine added. ID: {med_id} | {name} | Qty: {quantity} | Price: {price:.2f}")
    except ValueError:
        print("Invalid input! Please enter numeric values for quantity and price.")

def view_stock(medicines):
    
    if not medicines:
        print("Inventory is empty.")
        return
    print("\n--- Current Inventory Stock ---")
    print(f"{'ID':<6} | {'Name':<15} | {'Quantity':<10} | {'Price':<8}")
    print("-" * 48)
    for med in medicines:
        print(f"{med['ID']:<6} | {med['Name']:<15} | {med['Quantity']:<10} | {med['Price']:<8.2f}")
    print("-" * 48)

def sell_medicine(medicines):
    
    view_stock(medicines)
    med_id = input("ID: ").strip().upper()
    
    target_med = None
    for med in medicines:
        if med["ID"] == med_id:
            target_med = med
            break
            
    if not target_med:
        print("Error: Medicine ID not found.")
        return
        
    try:
        qty_to_sell = int(input("Quantity: "))
        if qty_to_sell < 0:
            print("Error: Quantity cannot be negative.")
            return
            
        if qty_to_sell > target_med["Quantity"]:
            print(f"Insufficient stock. Available: {target_med['Quantity']}")
            return
            
        target_med["Quantity"] -= qty_to_sell
        bill = qty_to_sell * target_med["Price"]
        save_medicines(medicines)
        
        print(f"Sold {qty_to_sell} units. Bill: {bill:.2f}")
        if target_med["Quantity"] == 0:
            print("Stock left: 0 | Out of stock!")
        else:
            print(f"Stock left: {target_med['Quantity']}")
    except ValueError:
        print("Invalid quantity input.")

def delete_medicine(medicines):
    
    med_id = input("ID: ").strip().upper()
    target_med = None
    for med in medicines:
        if med["ID"] == med_id:
            target_med = med
            break
            
    if target_med:
        medicines.remove(target_med)
        save_medicines(medicines)
        print(f"Medicine {med_id} deleted.")
    else:
        print(f"Error: Medicine ID {med_id} not found.")

def low_stock_report(medicines):
    
    print("\n--- Low Stock Report (Threshold: < 10) ---")
    found = False
    for med in medicines:
        if med["Quantity"] < 10:
            print(f"(a) {med['ID']} | {med['Name']} | Qty: {med['Quantity']} (Low stock)")
            found = True
    if not found:
        print("No items under low stock threshold.")

def total_inventory_value(medicines):
    
    total_value = sum(med["Quantity"] * med["Price"] for med in medicines)
    print(f"(c) Total inventory value: {total_value:.2f}")

def main():
    initialize_file()
    while True:
        medicines = load_medicines()
        print("\n==============================")
        print("   PHARMACY INVENTORY SYSTEM  ")
        print("==============================")
        print("1. Add Medicine")
        print("2. View Stock")
        print("3. Sell Medicine")
        print("4. Delete Medicine")
        print("5. Low Stock Report")
        print("6. Total Inventory Value")
        print("7. Exit")
        
        choice = input("Enter your menu option choice (1-7): ").strip()
        
        if choice == '1':
            add_medicine(medicines)
        elif choice == '2':
            view_stock(medicines)
        elif choice == '3':
            sell_medicine(medicines)
        elif choice == '4':
            delete_medicine(medicines)
        elif choice == '5':
            low_stock_report(medicines)
        elif choice == '6':
            total_inventory_value(medicines)
        elif choice == '7':
            print("Exiting Pharmacy Inventory System. Goodbye!")
            break
        else:
            print("Invalid option! Please choose between 1 and 7.")

if __name__ == "__main__":
    main()
1
