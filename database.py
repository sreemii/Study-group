from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import User, Base  # Import Base for table creation

DATABASE_URL = "sqlite:///./study_group.db"

# Create Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# Fetch User by Email
def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    print(f"User found in DB: {user}")  # 🔍 Debugging log
    return user

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
