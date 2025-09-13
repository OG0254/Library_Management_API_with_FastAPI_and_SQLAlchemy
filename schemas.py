from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# ------------------ MEMBER SCHEMAS ------------------
class MemberBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    join_date: Optional[date] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(MemberBase):
    pass

class MemberOut(MemberBase):
    member_id: int

    class Config:
        orm_mode = True

# ------------------ BOOK SCHEMAS ------------------
class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    book_id: int
    available_copies: int

    class Config:
        orm_mode = True

# ------------------ BORROWED BOOKS SCHEMAS ------------------
class BorrowedBookBase(BaseModel):
    member_id: int
    book_id: int
    borrow_date: date
    return_date: Optional[date] = None

class BorrowedBookCreate(BorrowedBookBase):
    pass

class BorrowedBookUpdate(BorrowedBookBase):
    pass

class BorrowedBookOut(BorrowedBookBase):
    borrow_id: int

    class Config:
        orm_mode = True

# ------------------ LIBRARIAN SCHEMAS ------------------
class LibrarianBase(BaseModel):
    full_name: str
    hire_date: date

class LibrarianCreate(LibrarianBase):
    pass

class LibrarianUpdate(LibrarianBase):
    pass

class LibrarianOut(LibrarianBase):
    librarian_id: int

    class Config:
        orm_mode = True

# ------------------ LIBRARIAN ACCOUNT SCHEMAS ------------------
class LibrarianAccountBase(BaseModel):
    username: str

class LibrarianAccountCreate(LibrarianAccountBase):
    librarian_id: int
    password_hash: str

class LibrarianAccountUpdate(LibrarianAccountBase):
    password_hash: Optional[str] = None

class LibrarianAccountOut(LibrarianAccountBase):
    account_id: int
    librarian_id: int

    class Config:
        orm_mode = True
