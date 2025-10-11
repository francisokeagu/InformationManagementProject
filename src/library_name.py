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


"""""""""""""""""MEDIUM"""""""""""""""
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






""""""""""""""""" COMPLEX """""""""""""""
#search books
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

