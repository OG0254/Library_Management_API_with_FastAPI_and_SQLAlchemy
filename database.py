from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Database URL for MySQL
# Format: "mysql+pymysql://username:password@host:port/database_name"
DATABASE_URL = "mysql+pymysql://root:Mossaico%25123%23@localhost:3306/library_db"

# 2. Create engine
engine = create_engine(DATABASE_URL)

# 3. SessionLocal class
# Used to interact with the DB (like opening/closing connections)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class for our models
# All ORM models (tables) will inherit from this
Base = declarative_base()
