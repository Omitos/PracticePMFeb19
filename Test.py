import sqlite3
from datetime import datetime


# Database setup
def setup_database():
    conn = sqlite3.connect("lost_found.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            location TEXT,
            date_found TEXT,
            claimed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


# Function to report a found item
def report_item():
    name = input("Enter item name: ")
    category = input("Enter category: ")
    location = input("Enter location found: ")
    date_found = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("lost_found.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, category, location, date_found) VALUES (?, ?, ?, ?)",
                   (name, category, location, date_found))
    conn.commit()
    conn.close()
    print("Item reported successfully!\n")


# Function to search for lost items
def search_items():
    search_term = input("Enter item name or category to search: ")
    conn = sqlite3.connect("lost_found.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name LIKE ? OR category LIKE ?", (f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    conn.close()

    if results:
        print("\nMatching Items:")
        for item in results:
            status = "Claimed" if item[5] else "Unclaimed"
            print(
                f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Location: {item[3]}, Date: {item[4]}, Status: {status}")
    else:
        print("No matching items found.")
    print()


# Function to view all unclaimed items
def view_unclaimed():
    conn = sqlite3.connect("lost_found.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE claimed = 0")
    results = cursor.fetchall()
    conn.close()

    if results:
        print("\nUnclaimed Items:")
        for item in results:
            print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Location: {item[3]}, Date: {item[4]}")
    else:
        print("No unclaimed items found.")
    print()


# Function to claim an item
def claim_item():
    item_id = input("Enter the ID of the item you want to claim: ")
    conn = sqlite3.connect("lost_found.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET claimed = 1 WHERE id = ? AND claimed = 0", (item_id,))
    if cursor.rowcount > 0:
        print("Item successfully claimed!\n")
    else:
        print("Invalid ID or item already claimed.\n")
    conn.commit()
    conn.close()


# Menu function
def menu():
    setup_database()
    while True:
        print("\nLost & Found System")
        print("1. Report a Found Item")
        print("2. Search for a Lost Item")
        print("3. View All Unclaimed Items")
        print("4. Claim an Item")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            report_item()
        elif choice == "2":
            search_items()
        elif choice == "3":
            view_unclaimed()
        elif choice == "4":
            claim_item()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    menu()
