""" Main Function Library """


# src/main_function_library_.py
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

#search books
from typing import List, Dict, Any, Optional, Tuple
import unicodedata
import difflib

def _normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip().lower()
    # remove diacritics: “François” -> “francois”
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

def _tokenize(s: str) -> List[str]:
    return [t for t in _normalize_text(s).replace("-", " ").replace("/", " ").split() if t]

def search_books(
    query: str,
    books_list: List[Dict[str, Any]],
    *,
    fields: Tuple[str, ...] = ("title", "author", "isbn"),
    fuzzy: bool = True,
    min_ratio: float = 0.65,     # 0..1 similarity threshold when fuzzy=True
    limit: Optional[int] = 25,   # max results
    page: int = 1,               # 1-based page index
    page_size: Optional[int] = None  # overrides 'limit' with paged results if set
) -> Dict[str, Any]:
    """
    Weighted, robust search across title/author/ISBN with optional fuzzy matching.

    Returns:
        {
          "total": int,
          "results": [book, ...],
          "page": int,
          "page_size": Optional[int]
        }
    """
    if not isinstance(query, str) or not query.strip():
        return {"total": 0, "results": [], "page": 1, "page_size": page_size}

    qnorm = _normalize_text(query)
    qtokens = set(_tokenize(query))

    # Weights: tune to preference
    weights = {"title": 1.0, "author": 0.7, "isbn": 0.9}

    scored: List[Tuple[float, Dict[str, Any]]] = []

    for book in books_list:
        score = 0.0
        for f in fields:
            val = _normalize_text(book.get(f, ""))
            if not val:
                continue

            # Exact/substring boost
            if qnorm in val:
                score += weights.get(f, 0.5) * (1.0 if val == qnorm else 0.85)

            # Token overlap boost (partial word hits)
            if qtokens:
                tokens = set(_tokenize(val))
                overlap = len(qtokens & tokens)
                if overlap:
                    score += weights.get(f, 0.5) * min(0.75, 0.15 * overlap)

            # Fuzzy matching (title/author mostly)
            if fuzzy and f in ("title", "author"):
                ratio = difflib.SequenceMatcher(None, qnorm, val).ratio()
                if ratio >= min_ratio:
                    # taper influence so near-perfect matches bubble up
                    score += weights.get(f, 0.5) * (ratio ** 2)

        if score > 0:
            scored.append((score, book))

    # sort by score desc, then title asc to stabilize order
    scored.sort(key=lambda x: (-x[0], _normalize_text(x[1].get("title", ""))))
    all_results = [b for _, b in scored]

    # Pagination logic
    if page_size is not None and page_size > 0:
        start = (max(page, 1) - 1) * page_size
        end = start + page_size
        page_results = all_results[start:end]
        return {"total": len(all_results), "results": page_results, "page": max(page, 1), "page_size": page_size}

    # Legacy limit behavior
    if limit is not None and limit > 0:
        all_results = all_results[:limit]

    return {"total": len(scored), "results": all_results, "page": 1, "page_size": None}



