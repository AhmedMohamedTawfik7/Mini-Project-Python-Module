from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Dict
from .models import User, Book, Category, Rating, ReadingHistory, Recommendation
from .enums import ReadingStatus

class LibraryManager:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.books: Dict[int, Book] = {}
        self.categories: Dict[int, Category] = {}
        self.ratings: List[Rating] = []
        self.history: List[ReadingHistory] = []
        self.recommendations: List[Recommendation] = []

    # ---- Add with validation ----
    def add_category(self, category: Category):
        if category.id in self.categories:
            raise ValueError(f"Category ID {category.id} already exists")
        if any(c.name.lower() == category.name.lower() for c in self.categories.values()):
            raise ValueError(f"Category name '{category.name}' duplicate")
        self.categories[category.id] = category

    def add_user(self, user: User):
        if user.id in self.users:
            raise ValueError(f"User ID {user.id} exists")
        if any(u.email == user.email for u in self.users.values()):
            raise ValueError(f"Email {user.email} already used")
        self.users[user.id] = user

    def add_book(self, book: Book):
        if book.id in self.books:
            raise ValueError(f"Book ID {book.id} exists")
        if book.category_id not in self.categories:
            raise ValueError(f"Category ID {book.category_id} not found - connect using IDs!")
        self.books[book.id] = book

    def add_rating(self, rating: Rating):
        if rating.user_id not in self.users or rating.book_id not in self.books:
            raise ValueError("user_id or book_id not linked correctly")
        # prevent duplicate rating from same user for same book (update instead)
        for r in self.ratings:
            if r.user_id == rating.user_id and r.book_id == rating.book_id:
                r.score = rating.score
                r.review = rating.review
                return
        self.ratings.append(rating)

    def add_reading(self, record: ReadingHistory):
        if record.user_id not in self.users or record.book_id not in self.books:
            raise ValueError("Invalid IDs in reading history")
        book = self.books[record.book_id]
        # Detect already read & manage copies
        if record.status == ReadingStatus.BORROWED:
            if book.available_copies <= 0:
                raise ValueError(f"No copies left for {book.title}")
            book.available_copies -= 1
        elif record.status == ReadingStatus.RETURNED:
            book.available_copies += 1
        
        self.history.append(record)

    # ---- Display / Search ----
    def search_books(self, query: str):
        q = query.lower()
        results = []
        for b in self.books.values():
            cat_name = self.categories.get(b.category_id).name.lower() if b.category_id in self.categories else ""
            if q in b.title.lower() or q in b.author.lower() or q in cat_name:
                results.append(b)
        return results

    def get_user_history(self, user_id: int) -> List[ReadingHistory]:
        return [h for h in self.history if h.user_id == user_id]

    def has_read(self, user_id: int, book_id: int) -> bool:
        return any(h.user_id == user_id and h.book_id == book_id and h.status in 
                   [ReadingStatus.COMPLETED, ReadingStatus.BORROWED, ReadingStatus.RETURNED] 
                   for h in self.history)

    # ---- Analytics (manual avg, Counter) ----
    def average_rating(self, book_id: int) -> float:
        scores = [r.score for r in self.ratings if r.book_id == book_id]
        if not scores: return 0.0
        # manual calculation - don't use statistics.mean per task
        total = 0
        for s in scores: total += s
        return total / len(scores)

    def popular_categories(self, top_n=3):
        # Counter for categories from history + ratings
        cat_ids = []
        for h in self.history:
            book = self.books.get(h.book_id)
            if book: cat_ids.append(book.category_id)
        counter = Counter(cat_ids)
        return counter.most_common(top_n)

    def popular_authors(self, top_n=3):
        authors = [self.books[h.book_id].author for h in self.history if h.book_id in self.books]
        return Counter(authors).most_common(top_n)

    def user_favorite_categories(self, user_id: int):
        user_books = [h.book_id for h in self.history if h.user_id == user_id]
        cat_ids = [self.books[bid].category_id for bid in user_books if bid in self.books]
        # also consider high ratings >=7
        high_rated = [r.book_id for r in self.ratings if r.user_id == user_id and r.score >= 7]
        cat_ids += [self.books[bid].category_id for bid in high_rated if bid in self.books]
        if not cat_ids: return []
        return [cid for cid, _ in Counter(cat_ids).most_common()]

    # ---- Recommendation Engine ----
    def recommend(self, user_id: int, limit=5) -> List[Recommendation]:
        if user_id not in self.users:
            raise ValueError("User not found")
        fav_cats = self.user_favorite_categories(user_id)
        if not fav_cats:
            # fallback to popular categories
            fav_cats = [cid for cid, _ in self.popular_categories()]

        recs = []
        for book in self.books.values():
            if self.has_read(user_id, book.id):
                continue
            score = 0
            reason_parts = []
            if book.category_id in fav_cats:
                # higher score for top fav cat
                rank = fav_cats.index(book.category_id)
                score += (len(fav_cats) - rank) * 2
                cat_name = self.categories[book.category_id].name
                reason_parts.append(f"favorite category '{cat_name}'")

            avg = self.average_rating(book.id)
            if avg >= 7:
                score += avg / 2
                reason_parts.append(f"high rating {avg:.1f}/10")

            if score > 0:
                recs.append(Recommendation(user_id, book.id, ", ".join(reason_parts), round(score, 2)))

        recs.sort(key=lambda r: r.score, reverse=True)
        self.recommendations = recs[:limit]
        return self.recommendations
