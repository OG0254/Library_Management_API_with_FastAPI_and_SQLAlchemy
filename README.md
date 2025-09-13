# Library Management API with FastAPI & SQLAlchemy

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Project Structure](#project-structure)  
3. [Prerequisites](#prerequisites)  
4. [Setup Instructions](#setup-instructions)  
5. [Database Configuration](#database-configuration)  
6. [Running the API](#running-the-api)  
7. [API Endpoints](#api-endpoints)  
    - [Members](#members)  
    - [Books](#books)  
    - [Borrowed Books](#borrowed-books)  
    - [Librarians](#librarians)  
    - [Librarian Accounts](#librarian-accounts)  
8. [Testing the API](#testing-the-api)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## Project Overview
This project is a **Library Management API** built with **FastAPI** and **SQLAlchemy**. It allows you to manage:

- **Members** – library users  
- **Books** – library books  
- **Borrowed Books** – track book borrowings  
- **Librarians** – staff managing the library  
- **Librarian Accounts** – login credentials for librarians  

The API supports **CRUD operations** for all entities.

---

## Project Structure

```
fastapi_crud/
├── main.py              # FastAPI application with all routes
├── models.py            # SQLAlchemy models for DB tables
├── schemas.py           # Pydantic schemas for request/response validation
├── database.py          # SQLAlchemy engine & session configuration
├── requirements.txt     # Project dependencies
└── README.md            # This file
```

---

## Prerequisites
Before running this project, make sure you have:

1. Python 3.10+ installed  
2. MySQL server installed and running  
3. A MySQL database created, e.g., `library_db`  
4. Git installed (optional, for cloning)  

---

## Setup Instructions

1. **Clone the repository (if using Git):**
```bash
git clone https://github.com/yourusername/library-api.git
cd library-api
```

2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## Database Configuration

1. Open `database.py` and set your **MySQL credentials**:

```python
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/library_db"
```

2. Make sure the database exists. You can create it with:

```sql
CREATE DATABASE library_db;
```

3. The `Base.metadata.create_all(bind=engine)` line in `main.py` ensures all tables are created automatically.

---

## Running the API

Start the FastAPI server using **uvicorn**:

```bash
uvicorn main:app --reload
```

- Open in browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- FastAPI automatically generates docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

---

## API Endpoints

### Members

| Method | Endpoint          | Description                  |
|--------|-----------------|------------------------------|
| POST   | /members/        | Create a new member          |
| GET    | /members/        | Get all members              |
| GET    | /members/{id}    | Get a single member by ID    |
| PUT    | /members/{id}    | Update member info           |
| DELETE | /members/{id}    | Delete a member              |

**Example: Create Member**
```json
POST /members/
{
  "full_name": "John Doe",
  "email": "john@example.com"
}
```

---

### Books

| Method | Endpoint       | Description                  |
|--------|----------------|------------------------------|
| POST   | /books/        | Create a new book            |
| GET    | /books/        | Get all books                |
| GET    | /books/{id}    | Get a single book by ID      |
| PUT    | /books/{id}    | Update book info             |
| DELETE | /books/{id}    | Delete a book                |

**Example: Create Book**
```json
POST /books/
{
  "title": "Python 101",
  "author": "Brian Ogada",
  "genre": "Programming",
  "published_year": 2025,
  "total_copies": 10
}
```

---

### Borrowed Books

| Method | Endpoint            | Description                  |
|--------|-------------------|------------------------------|
| POST   | /borrowed_books/   | Record a book borrowing      |
| GET    | /borrowed_books/   | Get all borrowed books       |
| GET    | /borrowed_books/{id}| Get a borrowed record       |
| PUT    | /borrowed_books/{id}| Update return date          |
| DELETE | /borrowed_books/{id}| Delete borrowed record      |

---

### Librarians

| Method | Endpoint       | Description                  |
|--------|----------------|------------------------------|
| POST   | /librarians/   | Create librarian             |
| GET    | /librarians/   | Get all librarians           |
| GET    | /librarians/{id}| Get a single librarian      |
| PUT    | /librarians/{id}| Update librarian info       |
| DELETE | /librarians/{id}| Delete librarian            |

---

### Librarian Accounts

| Method | Endpoint             | Description                  |
|--------|--------------------|------------------------------|
| POST   | /librarian_accounts/ | Create account for librarian |
| GET    | /librarian_accounts/ | Get all accounts             |
| GET    | /librarian_accounts/{id}| Get single account        |
| PUT    | /librarian_accounts/{id}| Update account            |
| DELETE | /librarian_accounts/{id}| Delete account            |

---

## Testing the API

You can test endpoints using:

1. **FastAPI docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
2. **Postman**: Send requests to `http://127.0.0.1:8000/`  
3. **cURL**:

```bash
curl -X POST "http://127.0.0.1:8000/members/" -H "Content-Type: application/json" -d '{"full_name": "John Doe", "email": "john@example.com"}'
```

---

## Contributing

1. Fork the repository  
2. Create a new branch `feature/your-feature`  
3. Make your changes  
4. Submit a Pull Request  

---

## License

This project is **open source** and available under the [MIT License](https://opensource.org/licenses/MIT).

