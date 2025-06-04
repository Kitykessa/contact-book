import csv
import os.path
import pandas as pd
import re
from tabulate import tabulate
from email_validator import validate_email, EmailNotValidError

CSV_FILE = "contacts.csv"

def main():
    if not os.path.isfile(CSV_FILE):
        df = pd.DataFrame(columns=["Name", "Email", "Number"])
        df["Number"] = df["Number"].astype(str)
        df.to_csv(CSV_FILE, index=False)

    print("Welcome to Contact Book")

    while True:
        print("-"*30)
        print("1. Add contact.")
        print("2. Delete contact.")
        print("3. Search contact.")
        print("4. Load all contacts.")
        print("5. Update contact.")
        print("0. Exit.")
        print("-"*30)

        choose = input("Choose an action: ")

        if choose == "1":
            add_contact()
        elif choose == "2":
            delete_contact()
        elif choose == "3":
            search_contact()
        elif choose == "4":
            load_contacts()
        elif choose == "5":
            update_contact()
        elif choose == "0":
            print("Goodbye")
            break
        else:
            print("Invalid option. Try again")


def is_valid_number(number):
    return re.fullmatch(r"^\+\d{9,13}$", number)

def get_non_empty_input(promt):
    while True:
        value = input(promt).strip()
        if value:
            return value
        print("Field cannot be empty.")

def get_valid_email(promt):
    while True:
        email = input(promt).strip()
        try:
            validate_email(email)
            return email
        except EmailNotValidError as e:
            print(f"Invalid email: {e}")

def get_valid_number(promt):
    while True:
        number = input(promt).strip()
        if is_valid_number(number):
            return number
        print("Invalid number. It must start with '+' and contain 9 to 13 digits.")

def is_empty_book():
    if not os.path.isfile(CSV_FILE):
        return True
    df = pd.read_csv(CSV_FILE, dtype={"Number": str})
    return df.empty


def add_contact():
    name = get_non_empty_input("Enter a name: ").title()
    email = get_valid_email("Enter an email: ")
    number = get_valid_number("Enter a number(format +XXXXXXXXXX): ")


    df = pd.read_csv(CSV_FILE, dtype={"Number": str})
    duplicate = df[
        (df["Name"] == name) |
        (df["Email"] == email) |
        (df["Number"] == number)
    ]
    if not duplicate.empty:
        print("Contact with this name/email/number already exists.")
        return False

    new_row = pd.DataFrame([[name, email, number]], columns=["Name", "Email", "Number"])
    new_row.to_csv(CSV_FILE, mode="a", index=False, header=False)
    print("Contact added:", name, email, number)
    return True

def delete_contact():
    if is_empty_book():
        print("No contact found.")
        return False

    name = get_non_empty_input("Enter a name to delete: "). lower()

    df = pd.read_csv(CSV_FILE, dtype={"Number": str})
    match = df[df["Name"].str.lower().str.strip() == name]

    if match.empty:
        print("Contact not found")
        return False

    print("Found contact:")
    print(tabulate(match, headers="keys", tablefmt="grid", showindex=False))

    confirm = input("Are you sure you want to delete thin contact? (yes/no):").lower().strip()
    while confirm not in ["yes", "no", "y", "n"]:
        confirm = input("Please type 'yes' or 'no': ")

    if confirm in ["yes", "y"]:
        df = df.drop(match.index)
        df.to_csv(CSV_FILE, index=False)
        print("Contact deleted.")
        return True
    else:
        print("Deletion canceled.")
        return False

def search_contact():
    if is_empty_book():
        print("No contact found.")
        return False

    keyword = get_non_empty_input("Enter name, email or number to search: ").lower()

    df = pd.read_csv(CSV_FILE, dtype={"Number": str})
    df["Number"] = df["Number"].astype(str)

    matches = df[
        df["Name"].str.lower().str.contains(keyword, regex=False) |
        df["Email"].str.lower().str.contains(keyword, regex=False) |
        df["Number"].astype(str).str.contains(keyword, regex=False)
    ]
    if matches.empty:
        print("Contact not found.")
    else:
        print("Search results:")
        print(tabulate(matches, headers="keys", tablefmt="grid", showindex=False))

def load_contacts():
    if is_empty_book():
        print("No contact found.")
        return False
    df = pd.read_csv(CSV_FILE, index_col=False, dtype={"Number": str})
    print("All contacts:")
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))

def update_contact():
    if is_empty_book():
        print("No contact found.")
        return False

    name = get_non_empty_input("Enter a name to update: ").lower().strip()
    df = pd.read_csv(CSV_FILE, dtype={"Number": str})

    match = df[df["Name"].str.lower().str.strip() == name]
    if match.empty:
        print("Contact not found.")
        return False
    print("Found contact:")
    print(tabulate(match, headers="keys", tablefmt="grid", showindex=False))

    index = match.index[0]

    new_name = input("Enter new name (leave blank to keep current): ").title().strip()

    new_email = input("Enter new email (leave blank to keep current): ").strip()
    if new_email:
        while True:
            try:
                validate_email(new_email)
                if not df[(df.index != index) & (df["Email"].str.lower() == new_email.lower())].empty:
                    print("Another contact already uses this email.")
                    new_email = input("Enter new email (leave blank to keep current): ").strip()
                    if not new_email:
                        break
                    continue
                break
            except EmailNotValidError as e:
                print(f"Invalid email: {e}")
                new_email = input("Enter new email (leave blank to keep current): ").strip()
                if not new_email:
                    break

    new_number = input("Enter new number (leave blank to keep current): ").strip()
    if new_number:
        while True:
            if not is_valid_number(new_number):
                print("Invalid number. It must start with '+' and contain 9 to 13 digits.")
            elif not df[(df.index != index) & (df["Number"] == new_number)].empty:
                print("Another contact already uses this number")
            else:
                break

            new_number = input("Enter new number (leave blank to keep current): ").strip()
            if not new_number:
                break

    print("Summary of changes:")
    current_name = df.at[index, "Name"]
    current_email = df.at[index, "Email"]
    current_number = df.at[index, "Number"]

    name_display = new_name if new_name else current_name
    email_display = new_email if new_email else current_email
    number_display = new_number if new_number else current_number

    print(f"Name: {current_name} --> {name_display}")
    print(f"Email: {current_email} --> {email_display}")
    print(f"Number: {current_number} --> {number_display}")

    if new_name:
        df.at[index, "Name"] = new_name
    if new_email:
        df.at[index, "Email"] = new_email
    if new_number:
        df.at[index, "Number"] = new_number

    df.to_csv(CSV_FILE, index=False)
    print("Contact updated.")
    return True

if __name__ == "__main__":
    main()
