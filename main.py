"""
Entry point - simple CLI demo for the task.
Run: python main.py
"""
from library import LibraryManager, User, Book, Category, Rating, ReadingHistory, ReadingStatus, JsonStorage

def demo():
    mgr = LibraryManager()
    storage = JsonStorage()
    storage.load(mgr)

    if not mgr.categories:
        # Seed data only if empty
        mgr.add_category(Category(1, "Science Fiction"))
        mgr.add_category(Category(2, "Fantasy"))
        mgr.add_category(Category(3, "History"))
        mgr.add_user(User(1, "Ahmed", "ahmed@example.com"))
        mgr.add_user(User(2, "Sara", "sara@example.com"))
        mgr.add_book(Book(101, "Dune", "Frank Herbert", 1, 3))
        mgr.add_book(Book(102, "The Hobbit", "J.R.R. Tolkien", 2, 2))
        mgr.add_book(Book(103, "Sapiens", "Yuval Noah Harari", 3, 1))
        mgr.add_rating(Rating(1, 101, 9, "Masterpiece"))
        mgr.add_rating(Rating(2, 102, 8, "Loved it"))
        mgr.add_reading(ReadingHistory(1, 101, ReadingStatus.COMPLETED))
        mgr.add_reading(ReadingHistory(1, 102, ReadingStatus.BORROWED))

    print("=== Users ===")
    for u in mgr.users.values(): print(u.to_dict())
    print("\n=== Books ===")
    for b in mgr.books.values(): 
        print(f"{b.title} by {b.author} | copies: {b.available_copies} | avg rating: {mgr.average_rating(b.id):.1f}")

    print("\n=== Search 'dune' ===")
    print([b.title for b in mgr.search_books("dune")])

    print("\n=== Reading history for user 1 ===")
    for h in mgr.get_user_history(1): print(h.to_dict())

    print("\n=== Popular categories ===", mgr.popular_categories())
    print("Popular authors ===", mgr.popular_authors())

    print("\n=== Recommendations for Ahmed ===")
    recs = mgr.recommend(1)
    for r in recs:
        book = mgr.books[r.book_id]
        print(f"- {book.title} (score {r.score}) reason: {r.reason}")

    storage.save(mgr)
    print("\nSaved to library/data/library.json")

if __name__ == "__main__":
    demo()
