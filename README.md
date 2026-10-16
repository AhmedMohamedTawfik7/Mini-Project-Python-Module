# Mini-Project-Python-Module – Small Online Library

Backend-style program managing users, books, categories, ratings, reading history and recommendations.

## Features required by task
- Classes: Users(ID,name,email), Books(ID,title,author,category,available copies), Categories, Ratings(userID,bookID,score,review), Reading History(userID,bookID,date,status), Recommendations(userID,bookID,reason,score)
- Add/display users & books
- Search by title/author/category
- Ratings 1..10 + review
- Enum for status: borrowed/completed/returned/wishlist
- User reading history
- Recommendations based on favorite categories + high ratings
- Detect already read
- Save/load as JSON
- Challenging points: Counter for popular cats/authors, datetime, properties, manual avg

## VS Code Setup
1. Open folder in VS Code: `File > Open Folder > Mini-Project-Python-Module`
2. Create venv: `python -m venv .venv` -> Select interpreter `Ctrl+Shift+P > Python: Select Interpreter > .venv`
3. Install: `pip install -r requirements.txt` (if any)

## Safe Git + GitHub workflow (no leaking secrets)
1. `git init`
2. Check `.gitignore` includes `.env`, `venv/`, `__pycache__/`, `library/data/*.json` (we provide)
3. `git status` BEFORE every commit - ensure no .env
4. `git add .gitignore README.md library/ main.py`
5. `git commit -m "feat: initial structure with models, enums, .gitignore"`
6. Create repo on GitHub (private or public) - DO NOT add .env there
7. `git remote add origin https://github.com/<you>/Mini-Project-Python-Module.git`
8. `git branch -M main`
9. `git push -u origin main`

### Commit plan (as requested: one task per commit)
- commit 1: `feat: core classes with properties validation`
- commit 2: `feat: library manager add/display + ID linking`
- commit 3: `feat: search and validation (email, rating, copies, duplicates)`
- commit 4: `feat: ratings + reading history + Enum + available_copies logic`
- commit 5: `feat: analytics Counter + average rating manual + popular`
- commit 6: `feat: recommendations + has_read detection`
- commit 7: `feat: JSON save/load persistence`
- commit 8: `docs: final README + SQLite research note` (optional bonus: sqlite)

## How to run
`python main.py`

Data persists to `library/data/library.json` (gitignored, so your personal test data won't leak)

## Security checklist
- [ ] No `.env` file committed
- [ ] `.gitignore` contains `.env`, `.venv`, `__pycache__`
- [ ] `git diff --cached` reviewed before push
- [ ] If you used real emails, keep data json gitignored

## SQLite bonus research
See `JsonStorage.export_to_sqlite_hint()` - create tables with FOREIGN KEYs for user_id, book_id, category_id. Store Enum as TEXT, datetime as ISO TEXT.
