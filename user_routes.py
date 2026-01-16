from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login")
def login_user(name: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.name == name,
        models.User.password == password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name
    }

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
