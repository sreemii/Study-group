from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from core.security import get_current_user
from models import StudySession  

router = APIRouter(tags=["Sessions"])

# Dependency to Check Admin Access
def admin_required(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user

# Create a Session (Admin Only)
@router.post("/", response_model=schemas.StudySessionResponse, dependencies=[Depends(admin_required)])
def create_session(session_data: schemas.StudySessionCreate, db: Session = Depends(get_db)):
    """
    **Admin Access Required**  
    - Creates a **new session** for a study group.
    """
    new_session = models.StudySession(**session_data.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

#create a sessions
@router.post("/", response_model=schemas.StudySessionResponse)
def create_session(
    session_data: schemas.StudySessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create sessions.")

    new_session = models.StudySession(**session_data.dict())  # ✅ Use StudySession
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

#get all sessions
@router.get("/", response_model=list[schemas.StudySessionResponse])
def get_sessions(db: Session = Depends(get_db)):
    """
    **Public Access**  
    - Retrieves all study sessions.
    """
    return db.query(models.StudySession).all()

#get session by id
@router.get("/{session_id}", response_model=schemas.StudySessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """
    **Public Access**  
    - Retrieves a study session by its ID.
    """
    session = db.query(models.StudySession).filter(models.StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


# Delete a Session (Admin Only)
@router.delete("/{session_id}", dependencies=[Depends(admin_required)])
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """
    **Admin Access Required**  
    - Allows an admin to **delete any session**.
    """
    session = db.query(models.StudySession).filter(models.StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}
