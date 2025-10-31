import logging
import unicodedata
import difflib
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional


class SearchandDashboard:
    """
    Class to search a book dataset, format dates, and prepare for dashboard analytics.

    Attributes
    ----------
    _data_source : list
        A list of dictionaries representing books.

    Example
    -------
    >>> books = [
    ...     {"title": "Clean Code", "author": "Robert Martin", "isbn": "9780132350884"},
    ...     {"title": "Python Tricks", "author": "Dan Bader", "isbn": "9781775093305"}
    ... ]
    >>> sd = SearchandDashboard(books)
    >>> result = sd.search("clean")
    >>> result["total"]
    1
    """

    def __init__(self, data_source: List[Dict[str, Any]]):
        if not isinstance(data_source, list):
            raise TypeError("data_source must be a list of dictionaries")
        self._data_source = data_source  # private attribute

    # ---------- Properties for Controlled Access ----------
    @property
    def data_source(self) -> List[Dict[str, Any]]:
        """Return the dataset."""
        return self._data_source

    @data_source.setter
    def data_source(self, new_data: List[Dict[str, Any]]):
        if not isinstance(new_data, list):
            raise TypeError("data_source must be a list of dictionaries")
        self._data_source = new_data

    # ---------- Utility Methods ----------
    @staticmethod
    def format_date(date_obj: datetime) -> str:
        """Format a datetime object as YYYY-MM-DD."""
        return date_obj.strftime("%Y-%m-%d") if date_obj else ""

    @staticmethod
    def _normalize_text(s: str) -> str:
        """Normalize string by lowercasing and removing accents."""
        if s is None:
            return ""
        s = str(s).strip().lower()
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

    @classmethod
    def _tokenize(cls, s: str) -> List[str]:
        """Convert string to list of tokens."""
        return [
            t for t in cls._normalize_text(s).replace("-", " ").replace("/", " ").split()
            if t
        ]

    # ---------- Core Search Method ----------
    def search(
        self,
        query: str,
        *,
        fields: Tuple[str, ...] = ("title", "author", "isbn"),
        fuzzy: bool = True,
        min_ratio: float = 0.65,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """
        Search for books by title, author, or ISBN with fuzzy matching.

        Parameters
        ----------
        query : str
            Search string
        limit : int
            Maximum results returned

        Returns
        -------
        dict: search results

        Example
        -------
        >>> sd.search("python")["total"]
        1
        """

        if not isinstance(query, str) or not query.strip():
            return {"total": 0, "results": []}

        qnorm = self._normalize_text(query)
        qtokens = set(self._tokenize(query))

        weights = {"title": 1.0, "author": 0.7, "isbn": 0.9}
        scored = []

        for book in self._data_source:
            score = 0.0
            for f in fields:
                val = self._normalize_text(book.get(f, ""))
                if not val:
                    continue

                if qnorm in val:  # exact-ish match
                    score += weights.get(f, 0.5)

                overlap = len(qtokens & set(self._tokenize(val)))  # token overlap
                if overlap:
                    score += weights.get(f, 0.5) * min(0.75, 0.15 * overlap)

                if fuzzy and f in ("title", "author"):  # fuzzy
                    ratio = difflib.SequenceMatcher(None, qnorm, val).ratio()
                    if ratio >= min_ratio:
                        score += weights.get(f, 0.5) * (ratio ** 2)

            if score > 0:
                scored.append((score, book))

        scored.sort(key=lambda x: (-x[0], self._normalize_text(x[1].get("title", ""))))
        results = [b for _, b in scored][:limit]

        return {"total": len(results), "results": results}

    # ---------- Dashboard Stub ----------
    def generate_dashboard(self):
        """
        Placeholder for dashboard logic.
        """
        logging.info("Dashboard not implemented yet.")
        return "Dashboard feature coming soon!"

    # ---------- String Representations ----------
    def __str__(self):
        return f"SearchandDashboard with {len(self._data_source)} records"

    def __repr__(self):
        return f"SearchandDashboard(data_source_size={len(self._data_source)})"
