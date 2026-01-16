from datetime import datetime,timezone
from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/cases", tags=["Cases"])

@router.post("/", response_model=schemas.CaseResponse)
def create_case(
    user_id: int,
    case: schemas.CaseCreate,
    db: Session = Depends(get_db)
):
        # Optional: check user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_case = models.Case(
    
    title=case.title,
    description=case.description,
    location=case.location,
    crime_type=case.crime_type,
    severity=case.severity,
    date_reported=case.date_reported,
    user_id=user_id,
    created_at=datetime.now(timezone.utc)

)

  
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case

@router.get("/")
def get_cases(db: Session = Depends(get_db)):
    return db.query(models.Case).all()

@router.get("/by-user")
def get_cases_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Case).filter(
        models.Case.user_id == user_id
    ).all()
@router.get("/{case_id}")
def get_case_by_id(case_id: int, db: Session = Depends(get_db)):
    case = db.query(models.Case).filter(models.Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    return case