import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional, Tuple

# --- Configuration ---
DATABASE_URL = "sqlite:///app_users.db"
Base = declarative_base()
Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# --- SQLAlchemy Model ---
class User(Base):
    """Database model for application users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    # Hashed password storage is crucial for security
    hashed_password = Column(String, nullable=False)
    name = Column(String)

    def __repr__(self):
        return f"<User(username='{self.username}', name='{self.name}')>"

# --- Database Functions ---

def init_db():
    """
    Creates the database tables and ensures a default user exists for testing.
    This should only run once on application startup.
    """
    Base.metadata.create_all(bind=Engine)
    session = SessionLocal()
    
    try:
        # Check if the 'admin' user exists
        if session.query(User).filter(User.username == "admin").first() is None:
            
            # NOTE: In a real application, this secret should be stored in a secure secret manager
            # We are using a simple password ('safe_pass') for the demo.
            password = "safe_pass"
            
            # Hashing the password using bcrypt. This is MANDATORY.
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            
            admin_user = User(
                username="admin", 
                hashed_password=hashed_password, 
                name="System Administrator"
            )
            
            session.add(admin_user)
            session.commit()
            print("INFO: Default 'admin' user created.")
        
    except Exception as e:
        print(f"ERROR: Database initialization failed: {e}")
        session.rollback()
    finally:
        session.close()

def get_user_by_username(username: str) -> Optional[User]:
    """Retrieves a user object by username."""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.username == username).first()
        return user
    finally:
        session.close()

def add_user(username: str, password: str, name: str) -> bool:
    """Adds a new user to the database (structure defined for future signup)."""
    session = SessionLocal()
    try:
        if session.query(User).filter(User.username == username).first():
            return False # User already exists
            
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        new_user = User(
            username=username, 
            hashed_password=hashed_password, 
            name=name
        )
        session.add(new_user)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()
