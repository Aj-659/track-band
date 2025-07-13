from model1 import User
from database import SessionLocal
from sqlalchemy.orm import Session

def fetch_usernames():
    db: Session = SessionLocal()
    try:
        usernames = db.query(User.Username).all()
        print("Fetched usernames:", usernames)
    
    finally:
        db.close()