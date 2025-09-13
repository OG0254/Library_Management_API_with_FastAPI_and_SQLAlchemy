from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 1. Members Table
class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    join_date = Column(Date, nullable=False)

    # relationships
    borrowed_books = relationship("BorrowedBook", back_populates="member")


# 2. Books Table
class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(50))
    published_year = Column(Integer)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)

    # relationships
    borrowed_books = relationship("BorrowedBook", back_populates="book")


# 3. Borrowed Books Table (junction)
class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    borrow_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.member_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date)

    # relationships
    member = relationship("Member", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowed_books")


# 4. Librarians Table
class Librarian(Base):
    __tablename__ = "librarians"

    librarian_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=False)

    # relationships
    account = relationship("LibrarianAccount", back_populates="librarian", uselist=False)


# 5. Librarian Accounts Table (1-to-1 with librarians)
class LibrarianAccount(Base):
    __tablename__ = "librarian_accounts"

    account_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    librarian_id = Column(Integer, ForeignKey("librarians.librarian_id"), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)

    # relationships
    librarian = relationship("Librarian", back_populates="account")
