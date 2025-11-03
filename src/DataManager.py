import csv
import json
from typing import List, Dict, Any

class DataManager:
    """
    Manages data loading and catalog maintenance for the library system.

    This class interacts with the Catalog and LibraryItem classes to load data, create reports, and manage items.

    Methods
    -------
    load_library_data(source)
        Load items from a CSV/JSON file or a list of dicts into a Catalog.
    create_report(catalog)
        Generate a simple catalog report.
    add_new_book(catalog, *, item_id, title, isbn, loan_period=14)
        Add a new book to the catalog.
    remove_book(catalog, item_id)
        Remove a book from the catalog by its ID.
    """

    def load_library_data(self, source) -> 'Catalog':
        """Load library data from a CSV, JSON, or list of dicts into a Catalog."""
        catalog = Catalog()

        def _build_item(record: Dict[str, Any]) -> 'Library
