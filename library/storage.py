import json
import pathlib
from .models import User, Book, Category, Rating, ReadingHistory, Recommendation

class JsonStorage:
    def __init__(self, filepath="library/data/library.json"):
        self.filepath = pathlib.Path(filepath)

    def save(self, manager):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "users": [u.to_dict() for u in manager.users.values()],
            "books": [b.to_dict() for b in manager.books.values()],
            "categories": [c.to_dict() for c in manager.categories.values()],
            "ratings": [r.to_dict() for r in manager.ratings],
            "history": [h.to_dict() for h in manager.history],
            "recommendations": [r.to_dict() for r in manager.recommendations],
        }
        # Important: research JSON - datetime already converted to isoformat
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, manager):
        if not self.filepath.exists():
            return
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        manager.users = {d["id"]: User.from_dict(d) for d in data.get("users", [])}
        manager.categories = {d["id"]: Category.from_dict(d) for d in data.get("categories", [])}
        manager.books = {d["id"]: Book.from_dict(d) for d in data.get("books", [])}
        manager.ratings = [Rating.from_dict(d) for d in data.get("ratings", [])]
        manager.history = [ReadingHistory.from_dict(d) for d in data.get("history", [])]
        manager.recommendations = [Recommendation.from_dict(d) for d in data.get("recommendations", [])]

    # Bonus: SQLite research hint
    def export_to_sqlite_hint(self):
        return """
        Research: How to store this in SQLite?
        1. CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE)
        2. Use sqlite3.connect('library.db')
        3. Convert to_dict to rows, handle foreign keys category_id, user_id, book_id
        4. For Enum, store .value as TEXT
        5. For datetime, store isoformat TEXT
        """
