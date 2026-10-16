from enum import Enum

class ReadingStatus(str, Enum):
    """Research Task: Why Enum? It prevents typos like 'borrowd' vs 'borrowed'"""
    BORROWED = "borrowed"
    COMPLETED = "completed"
    RETURNED = "returned"
    WISHLIST = "wishlist"

    # Guiding question: Should you allow RETURNED to free up available_copies?
