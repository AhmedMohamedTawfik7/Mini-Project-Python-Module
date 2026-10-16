import re
from datetime import datetime
from collections import Counter
from .enums import ReadingStatus

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name.strip()

    def to_dict(self): return {"id": self.id, "name": self.name}
    @classmethod
    def from_dict(cls, d): return cls(d["id"], d["name"])

class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name.strip()
        self.email = email  # goes through setter
        self._email = None
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not EMAIL_REGEX.match(value):
            raise ValueError(f"Invalid email: {value}")
        self._email = value.lower()

    def to_dict(self): return {"id": self.id, "name": self.name, "email": self.email}
    @classmethod
    def from_dict(cls, d): return cls(d["id"], d["name"], d["email"])

class Book:
    def __init__(self, id: int, title: str, author: str, category_id: int, available_copies: int = 1):
        self.id = id
        self.title = title.strip()
        self.author = author.strip()
        self.category_id = category_id
        self._available_copies = 0
        self.available_copies = available_copies  # property

    @property
    def available_copies(self):
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("available_copies must be int >= 0")
        self._available_copies = value

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author, 
                "category_id": self.category_id, "available_copies": self.available_copies}
    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["title"], d["author"], d["category_id"], d["available_copies"])

class Rating:
    def __init__(self, user_id: int, book_id: int, score: int, review: str = ""):
        self.user_id = user_id
        self.book_id = book_id
        self._score = 0
        self.score = score
        self.review = review.strip()
        self.created_at = datetime.now()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int) or not (1 <= value <= 10):
            raise ValueError("Rating score must be 1..10")
        self._score = value

    def to_dict(self):
        return {"user_id": self.user_id, "book_id": self.book_id, 
                "score": self.score, "review": self.review,
                "created_at": self.created_at.isoformat()}
    @classmethod
    def from_dict(cls, d):
        obj = cls(d["user_id"], d["book_id"], d["score"], d.get("review",""))
        obj.created_at = datetime.fromisoformat(d["created_at"])
        return obj

class ReadingHistory:
    def __init__(self, user_id: int, book_id: int, status: ReadingStatus, date=None):
        self.user_id = user_id
        self.book_id = book_id
        if isinstance(status, str):
            status = ReadingStatus(status)
        self.status = status
        self.date = date or datetime.now()

    def to_dict(self):
        return {"user_id": self.user_id, "book_id": self.book_id,
                "status": self.status.value, "date": self.date.isoformat()}
    @classmethod
    def from_dict(cls, d):
        return cls(d["user_id"], d["book_id"], ReadingStatus(d["status"]), datetime.fromisoformat(d["date"]))

class Recommendation:
    def __init__(self, user_id: int, book_id: int, reason: str, score: float):
        self.user_id = user_id
        self.book_id = book_id
        self.reason = reason
        self.score = score

    def to_dict(self): return self.__dict__
    @classmethod
    def from_dict(cls, d): return cls(d["user_id"], d["book_id"], d["reason"], d["score"])
