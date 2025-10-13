""" Main Function Library """


# src/library_name.py
import pandas as pd
import logging
import os


"""""""""""""""" EASY  """""""""""""""
def setup_logger(logfile="app.log"):
    """Configure and initialize logging for the application."""
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logger initialized successfully.")




def generate_dashboard(data_source):
    """Integrate analytics and visualizations (placeholder for dashboard code)."""
    logging.info("Dashboard generation not yet implemented.")
    pass

def format_date(date_obj):
    """
    Format a datetime object as 'YYYY-MM-DD'.
    """
    return date_obj.strftime("%Y-%m-%d") if date_obj else ""

from datetime import timedelta

def get_due_date(checkout_date, loan_period=14):
    """
    Calculate the due date for a borrowed book.
    """
    return checkout_date + timedelta(days=loan_period)

def is_available(book_id, catalog):
    """
    Check if a book with the given ID is available.
    """
    for book in catalog:
        if book.get("id") == book_id:
            return book.get("available", False)
    return FalseI 



"""""""""""""""""MEDIUM"""""""""""""""

# Create Report
def create_report(data):
    """Generate a simple analytics summary for the dataset."""
    if data is None or data.empty:
        logging.warning("No data available for report.")
        return {}

    summary = {
        "total_records": len(data),
        "unique_users": data["user_id"].nunique() if "user_id" in data.columns else 0,
        "unique_titles": data["title"].nunique() if "title" in data.columns else 0
    }

    logging.info("Report created successfully.")
    return summary


# Load library data
def load_library_data(filepath):
    """Load and preprocess library data from a CSV file."""
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return None

    try:
        data = pd.read_csv(filepath)
        logging.info(f"Loaded data from {filepath}.")
        return data
    except Exception as e:
        logging.exception(f"Error loading data: {e}")
        return None
    
# Validate Input
def validate_input(data):
    """Ensure dataset structure and required columns are valid."""
    if data is None or data.empty:
        logging.error("Validation failed: Data is empty.")
        return False

    required_cols = ["user_id", "title", "checkout_date"]
    missing = [c for c in required_cols if c not in data.columns]
    if missing:
        logging.error(f"Missing required columns: {missing}")
        return False

    logging.info("Data validation passed.")

    return True


#Add new book
def add_new_book(book_data, catalog):
    """
    Validates and inserts a new book into the catalog.

    Args:
        book_data (dict): Dictionary containing book information.
        catalog (list): List of existing book dictionaries.

    Returns:
        list: Updated catalog list.
    """
    required_fields = ["title", "author", "isbn"]

    # Check required fields
    for field in required_fields:
        if field not in book_data or not book_data[field]:
            print(f"Missing required field: {field}")
            return catalog

    # Prevent duplicate ISBNs
    for book in catalog:
        if book["isbn"] == book_data["isbn"]:
            print(f"Book with ISBN {book_data['isbn']} already exists.")
            return catalog

    # Validate ISBN (basic)
    if not (len(book_data["isbn"]) in [10, 13] and book_data["isbn"].isdigit()):
        print(f"Invalid ISBN format: {book_data['isbn']}")
        return catalog

    # Add to catalog
    catalog.append(book_data)
    print(f"Added new book: {book_data['title']}")
    return catalog

# Checkout book(s)
from datetime import datetime, timedelta

def checkout_book(user_id, book_id, catalog, users, loan_period=14):
    """
    Allows a user to check out a book if available.

    Args:
        user_id (str): ID of the user borrowing the book.
        book_id (int): ID of the book to be borrowed.
        catalog (list): List of book dictionaries.
        users (list): List of user dictionaries.
        loan_period (int): Number of days before the book is due.

    Returns:
        tuple: (success: bool, message: str)
    """
    # 1. Validate user exists
    user = next((u for u in users if u.get("id") == user_id), None)
    if not user:
        return False, f"User ID '{user_id}' not found."

    # 2. Validate book exists
    book = next((b for b in catalog if b.get("id") == book_id), None)
    if not book:
        return False, f"Book ID '{book_id}' not found."

    # 3. Check availability
    if not book.get("available", True):
        return False, f"'{book['title']}' is currently unavailable."

    # 4. Prepare borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=loan_period)
    borrow_record = {
        "user_id": user_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": None
    }

    # 5. Update book record
    book["available"] = False
    if "borrow_history" not in book:
        book["borrow_history"] = []
    book["borrow_history"].append(borrow_record)

    # 6. Update user record
    if "borrowed_books" not in user:
        user["borrowed_books"] = []
    user["borrowed_books"].append({
        "book_id": book_id,
        "borrow_date": borrow_date,
        "due_date": due_date
    })

    # 7. Return success message
    msg = (
        f"{user['name']} successfully checked out '{book['title']}'. "
        f"Due on {due_date.strftime('%Y-%m-%d')}."
    )
    return True, msg

# Return book(s)
def return_book(user_id, book_id, catalog, users, daily_rate=0.25):
    """
    Handles book return, updates availability, and calculates late fees.

    Args:
        user_id (str): ID of the user returning the book.
        book_id (int): ID of the book being returned.
        catalog (list): List of book dictionaries.
        users (list): List of user dictionaries.
        daily_rate (float): Fee per day if book is overdue.

    Returns:
        tuple: (success: bool, message: str, fee: float)
    """
    # 1. Find user
    user = next((u for u in users if u.get("id") == user_id), None)
    if not user:
        return False, f"❌ User ID '{user_id}' not found.", 0.0

    # 2. Find book
    book = next((b for b in catalog if b.get("id") == book_id), None)
    if not book:
        return False, f"Book ID '{book_id}' not found.", 0.0

    # 3. Check if user actually borrowed this book
    borrowed_books = user.get("borrowed_books", [])
    record = next((r for r in borrowed_books if r["book_id"] == book_id), None)
    if not record:
        return False, f"Book ID '{book_id}' is not borrowed by user '{user_id}'.", 0.0

    # 4. Calculate late fee
    due_date = record["due_date"]
    return_date = datetime.now()
    days_late = max(0, (return_date - due_date).days)
    fee = days_late * daily_rate

    # 5. Update book availability
    book["available"] = True

    # 6. Update book borrow history
    for entry in book.get("borrow_history", []):
        if entry["user_id"] == user_id and entry["return_date"] is None:
            entry["return_date"] = return_date
            break

    # 7. Remove from user’s borrowed list
    user["borrowed_books"] = [r for r in borrowed_books if r["book_id"] != book_id]

    # 8. Return success message
    if days_late > 0:
        msg = f"'{book['title']}' returned late by {days_late} day(s). Fee: ${fee:.2f}."
    else:
        msg = f"'{book['title']}' returned on time. No fee."

    return True, msg, fee

def remove_book(book_id, catalog, permanent=False):
    """
    Remove or deactivate a book from the catalog.

    Args:
        book_id (int): ID of the book to remove.
        catalog (list): List of book dictionaries.
        permanent (bool): If True, delete permanently; otherwise mark as inactive.

    Returns:
        tuple: (success: bool, message: str)
    """
    # Find book by ID
    book = next((b for b in catalog if b.get("id") == book_id), None)
    if not book:
        return False, f"Book ID '{book_id}' not found."

    # Prevent removing a borrowed book
    if not book.get("available", True):
        return False, f"Cannot remove '{book['title']}' because it is currently borrowed."

    # Handle permanent or soft deletion
    if permanent:
        catalog.remove(book)
        return True, f"Book '{book['title']}' permanently removed from catalog."
    else:
        book["available"] = False
        book["removed"] = True
        return True, f"Book '{book['title']}' marked as inactive (soft removed)."




""""""""""""""""" COMPLEX """""""""""""""

# Search book(s)
def search_books(query, books_list):
    """
    Search for books in the catalog by title, author, or ISBN.

    Args:
        query (str): Search keyword (case-insensitive).
        books_list (list): List of book dictionaries.

    Returns:
        list: Matching books, or an empty list if none found.
    """
    if not query or not isinstance(query, str):
        print("Invalid search query.")
        return []

    query = query.lower().strip()
    results = []

    for book in books_list:
        # Ensure keys exist and convert to lowercase strings
        title = str(book.get("title", "")).lower()
        author = str(book.get("author", "")).lower()
        isbn = str(book.get("isbn", "")).lower()

        if query in title or query in author or query in isbn:
            results.append(book)

    if results:
        print(f"Found {len(results)} result(s) for '{query}':")
    else:
        print(f"No books found for '{query}'.")

    return results


# generate monthly report
from datetime import datetime
from collections import Counter, defaultdict

def generate_monthly_report(catalog, users):
    """
    Generate a monthly report of borrowing activity, top books, and user engagement.

    Args:
        catalog (list): List of book dictionaries, each with a 'borrow_history' list.
        users (list): List of user dictionaries with 'id' and 'name' fields.

    Returns:
        dict: Summary of monthly activity.
    """
    now = datetime.now()
    borrowed = Counter()
    activity = defaultdict(int)
    overdue = []

    # Iterate over all books and their borrow history
    for book in catalog:
        for rec in book.get('borrow_history', []):
            bd = rec.get('borrow_date')
            dd = rec.get('due_date')
            rd = rec.get('return_date')
            uid = rec.get('user_id')

            # Convert to datetime if given as string
            if isinstance(bd, str):
                bd = datetime.fromisoformat(bd)
            if isinstance(dd, str):
                dd = datetime.fromisoformat(dd)
            if isinstance(rd, str) and rd:
                rd = datetime.fromisoformat(rd)

            # Count only if borrowed this month
            if bd and bd.month == now.month and bd.year == now.year:
                borrowed[book.get('title', 'Unknown Title')] += 1
                if uid:
                    activity[uid] += 1

            # Track overdue (not returned and due date has passed)
            if not rd and dd and dd < now:
                overdue.append(book.get('title', 'Unknown Title'))

    # Map user IDs to names
    name_map = {u.get('id'): u.get('name') for u in users}
    active = [name_map.get(i, f"User {i}") for i in activity]
    inactive = [name_map.get(u.get('id')) for u in users if u.get('id') not in activity]

    # Build report data
    report = {
        "month": now.strftime("%B %Y"),
        "total_books": len(catalog),
        "total_users": len(users),
        "borrowed_this_month": sum(borrowed.values()),
        "top_borrowed": borrowed.most_common(5),
        "overdue_books": list(set(overdue)),
        "active_users": active,
        "inactive_users": inactive
    }

    # Print summary
    print(f"\n=== Monthly Report: {report['month']} ===")
    print(f"Total Books: {report['total_books']}")
    print(f"Total Users: {report['total_users']}")
    print(f"Borrowed This Month: {report['borrowed_this_month']}")
    print("Top Borrowed:", report['top_borrowed'])
    print("Overdue Books:", report['overdue_books'])
    print("Active Users:", report['active_users'])
    print("Inactive Users:", report['inactive_users'])

    return report

# import_books_from_csv function
import csv
from src.utils import validate_isbn, clean_input, format_book_title, normalize_author_name

def import_books_from_csv(filename, catalog):
    """
    Reads book records from a CSV file and adds valid entries to the catalog.

    Args:
        filename (str): Path to the CSV file.
        catalog (list): List of existing book dictionaries.

    Returns:
        tuple: (updated_catalog, summary_report)
    """
    added = 0
    skipped = 0

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = clean_input(row.get("title", ""))
                author = normalize_author_name(row.get("author", ""))
                isbn = clean_input(row.get("isbn", ""))
                year = row.get("year")
                available = str(row.get("available", "True")).lower() in ("true", "1", "yes")

                # Validate required fields
                if not title or not author or not isbn:
                    skipped += 1
                    continue

                # Check for duplicates by ISBN
                if any(b["isbn"] == isbn for b in catalog):
                    skipped += 1
                    continue

                # Validate ISBN format
                if not validate_isbn(isbn):
                    skipped += 1
                    continue

                # Add new book entry
                new_book = {
                    "id": len(catalog) + 1,
                    "title": format_book_title(title),
                    "author": author,
                    "isbn": isbn,
                    "year": int(year) if year and year.isdigit() else None,
                    "available": available,
                    "borrow_history": []
                }
                catalog.append(new_book)
                added += 1

    except FileNotFoundError:
        print(f"File not found: {filename}")
        return catalog, {"added": added, "skipped": skipped, "error": "File not found"}

    except Exception as e:
        print(f"Error reading file: {e}")
        return catalog, {"added": added, "skipped": skipped, "error": str(e)}

    print(f"Import complete — {added} added, {skipped} skipped.")
    return catalog, {"added": added, "skipped": skipped, "error": None}


