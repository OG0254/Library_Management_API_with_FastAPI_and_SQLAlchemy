from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from database import SessionLocal, engine, Base
from models import Member, Book, BorrowedBook, Librarian, LibrarianAccount
from schemas import (
    MemberCreate, MemberUpdate, MemberOut,
    BookCreate, BookUpdate, BookOut,
    BorrowedBookCreate, BorrowedBookUpdate, BorrowedBookOut,
    LibrarianCreate, LibrarianUpdate, LibrarianOut,
    LibrarianAccountCreate, LibrarianAccountUpdate, LibrarianAccountOut
)

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Full Library CRUD API")

# ------------------ Dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ MEMBERS CRUD ------------------
@app.post("/members/", response_model=MemberOut)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    new_member = Member(**member.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@app.get("/members/", response_model=List[MemberOut])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

@app.get("/members/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.put("/members/{member_id}", response_model=MemberOut)
def update_member(member_id: int, member_data: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in member_data.dict().items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
    return {"message": f"Member {member_id} deleted successfully"}

# ------------------ BOOKS CRUD ------------------
@app.post("/books/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict(), available_copies=book.total_copies)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_data.dict().items():
        setattr(book, key, value)
    # Adjust available copies if needed
    if book.available_copies > book.total_copies:
        book.available_copies = book.total_copies
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": f"Book {book_id} deleted successfully"}

# ------------------ BORROWED BOOKS CRUD ------------------
@app.post("/borrowed_books/", response_model=BorrowedBookOut)
def borrow_book(borrow_data: BorrowedBookCreate, db: Session = Depends(get_db)):
    # Check book availability
    book = db.query(Book).filter(Book.book_id == borrow_data.book_id).first()
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    book.available_copies -= 1
    borrowed_book = BorrowedBook(**borrow_data.dict())
    db.add(borrowed_book)
    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book

@app.get("/borrowed_books/", response_model=List[BorrowedBookOut])
def get_borrowed_books(db: Session = Depends(get_db)):
    return db.query(BorrowedBook).all()

@app.put("/borrowed_books/{borrow_id}", response_model=BorrowedBookOut)
def return_book(borrow_id: int, borrow_data: BorrowedBookUpdate, db: Session = Depends(get_db)):
    borrowed_book = db.query(BorrowedBook).filter(BorrowedBook.borrow_id == borrow_id).first()
    if not borrowed_book:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    for key, value in borrow_data.dict().items():
        setattr(borrowed_book, key, value)
    # Handle book return
    if borrow_data.return_date:
        book = db.query(Book).filter(Book.book_id == borrowed_book.book_id).first()
        if book:
            book.available_copies += 1
    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book

@app.delete("/borrowed_books/{borrow_id}")
def delete_borrowed_book(borrow_id: int, db: Session = Depends(get_db)):
    borrowed_book = db.query(BorrowedBook).filter(BorrowedBook.borrow_id == borrow_id).first()
    if not borrowed_book:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    # Increment available copies if returning before deletion
    book = db.query(Book).filter(Book.book_id == borrowed_book.book_id).first()
    if book:
        book.available_copies += 1
    db.delete(borrowed_book)
    db.commit()
    return {"message": f"Borrow record {borrow_id} deleted successfully"}

# ------------------ LIBRARIANS CRUD ------------------
@app.post("/librarians/", response_model=LibrarianOut)
def create_librarian(librarian: LibrarianCreate, db: Session = Depends(get_db)):
    new_librarian = Librarian(**librarian.dict())
    db.add(new_librarian)
    db.commit()
    db.refresh(new_librarian)
    return new_librarian

@app.get("/librarians/", response_model=List[LibrarianOut])
def get_librarians(db: Session = Depends(get_db)):
    return db.query(Librarian).all()

@app.get("/librarians/{librarian_id}", response_model=LibrarianOut)
def get_librarian(librarian_id: int, db: Session = Depends(get_db)):
    librarian = db.query(Librarian).filter(Librarian.librarian_id == librarian_id).first()
    if not librarian:
        raise HTTPException(status_code=404, detail="Librarian not found")
    return librarian

# ------------------ LIBRARIAN ACCOUNTS CRUD ------------------
@app.post("/librarian_accounts/", response_model=LibrarianAccountOut)
def create_librarian_account(account: LibrarianAccountCreate, db: Session = Depends(get_db)):
    new_account = LibrarianAccount(**account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@app.get("/librarian_accounts/", response_model=List[LibrarianAccountOut])
def get_librarian_accounts(db: Session = Depends(get_db)):
    return db.query(LibrarianAccount).all()
