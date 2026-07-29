expenses = []
expense_id = 1
FILE_NAME = "expenses.txt"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Healthcare",
    "Education",
    "Other",
]


def show_line():
    print("-" * 70)


def show_title(text):
    show_line()
    print(text.center(70))
    show_line()


def pause():
    input("\nPress Enter to continue...")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount (PKR): "))
            if amount > 0:
                return amount
            print("Amount must be more than zero.")
        except ValueError:
            print("Please type a number.")


def get_description():
    while True:
        description = input("Enter description: ").strip()
        if description:
            return description
        print("Please enter something.")


def choose_category():
    print("\nChoose a category:")
    show_line()

    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")

    show_line()

    while True:
        try:
            choice = int(input("Select a number: "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Please choose one of the numbers above.")
        except ValueError:
            print("Please type a number.")


def save_expenses():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for expense in expenses:
                file.write(f"{expense['id']},{expense['description']},{expense['amount']},{expense['category']}\n")
        print("\nYour expenses were saved.")
    except Exception as error:
        print("Something went wrong while saving.")
        print(error)


def load_expenses():
    global expense_id

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for record in file:
                record = record.strip()
                if not record:
                    continue

                data = record.split(",")
                if len(data) != 4:
                    continue

                expense = {
                    "id": int(data[0]),
                    "description": data[1],
                    "amount": float(data[2]),
                    "category": data[3],
                }

                expenses.append(expense)

                if expense["id"] >= expense_id:
                    expense_id = expense["id"] + 1

    except FileNotFoundError:
        pass
    except (ValueError, IndexError):
        print("The saved file looks a little messy, so it was skipped.")


def add_expense():
    global expense_id

    show_title("ADD NEW EXPENSE")

    description = get_description()
    amount = get_amount()
    category = choose_category()

    expenses.append({
        "id": expense_id,
        "description": description,
        "amount": amount,
        "category": category,
    })

    print("\nExpense added.")
    print(f"ID: {expense_id}")

    expense_id += 1
    pause()


def show_header():
    print("\n")
    print("=" * 70)
    print("PERSONAL EXPENSE TRACKER".center(70))
    print("=" * 70)


def show_table_header():
    print(f"{'ID':<6}{'DESCRIPTION':<25}{'CATEGORY':<18}{'AMOUNT':>15}")
    show_line()


def view_expenses():
    show_title("ALL EXPENSES")

    if not expenses:
        print("You do not have any expenses yet.")
        pause()
        return

    show_table_header()

    total = 0
    for expense in expenses:
        print(f"{expense['id']:<6}{expense['description']:<25}{expense['category']:<18}PKR {expense['amount']:>8.2f}")
        total += expense["amount"]

    show_line()
    print(f"{'TOTAL':<52}PKR {total:>8.2f}")
    pause()


def category_summary():
    show_title("CATEGORY SUMMARY")

    if not expenses:
        print("There is nothing to summarize yet.")
        pause()
        return

    summary = {}
    total_amount = 0

    for expense in expenses:
        category = expense["category"]
        summary[category] = summary.get(category, 0) + expense["amount"]
        total_amount += expense["amount"]

    print(f"{'CATEGORY':<20}{'AMOUNT':<18}{'PERCENTAGE'}")
    show_line()

    for category in sorted(summary):
        amount = summary[category]
        percentage = (amount / total_amount) * 100
        print(f"{category:<20}PKR {amount:<12.2f}{percentage:.2f}%")

    show_line()
    print(f"Grand Total: PKR {total_amount:.2f}")
    pause()


def filter_by_category():
    show_title("FILTER BY CATEGORY")

    category = choose_category()

    found = False
    total = 0

    show_table_header()

    for expense in expenses:
        if expense["category"] == category:
            found = True
            print(f"{expense['id']:<6}{expense['description']:<25}{expense['category']:<18}PKR {expense['amount']:>8.2f}")
            total += expense["amount"]

    if not found:
        print("\nNo expenses were found in that category.")
    else:
        show_line()
        print(f"{'CATEGORY TOTAL':<52}PKR {total:>8.2f}")

    pause()


def delete_expense():
    show_title("DELETE EXPENSE")

    if not expenses:
        print("There is nothing here to delete.")
        pause()
        return

    view_expenses()

    while True:
        try:
            delete_id = int(input("\nEnter the expense ID to delete: "))
            break
        except ValueError:
            print("Please enter a valid ID.")

    for expense in expenses:
        if expense["id"] == delete_id:
            confirm = input("Delete this expense? (Y/N): ").strip().upper()
            if confirm == "Y":
                expenses.remove(expense)
                print("\nExpense removed.")
            else:
                print("\nDeletion cancelled.")
            pause()
            return

    print("No expense matched that ID.")
    pause()


def show_menu():
    show_header()

    print("1. Add expense")
    print("2. View all expenses")
    print("3. Category summary")
    print("4. Filter by category")
    print("5. Delete expense")
    print("6. Save expenses")
    print("7. Exit")

    show_line()


def main():
    load_expenses()
    print(f"\nYou currently have {len(expenses)} saved expense(s).")

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            filter_by_category()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            save_expenses()
            pause()
        elif choice == "7":
            save_expenses()
            print("\nThanks for using the expense tracker.")
            break
        else:
            print("\nThat choice is not available.")
            pause()


if __name__ == "__main__":
    main()