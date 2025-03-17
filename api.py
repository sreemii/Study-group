from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, schemas

router = APIRouter(prefix="/groups", tags=["groups"])

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new study group (POST)
@router.post("/std", response_model=schemas.StudyGroupResponse)
def create_group(group: schemas.StudyGroupCreate, db: Session = Depends(get_db)):
    db_group = database.StudyGroup(name=group.name, description=group.description)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

# Get all study groups (GET)
@router.get("/std", response_model=list[schemas.StudyGroupResponse])
def get_groups(db: Session = Depends(get_db)):
    return db.query(database.StudyGroup).all()

# Update a study group (PUT)
@router.put("/std/{group_id}", response_model=schemas.StudyGroupResponse)
def update_group(group_id: int, group: schemas.StudyGroupCreate, db: Session = Depends(get_db)):
    db_group = db.query(database.StudyGroup).filter(database.StudyGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db_group.name = group.name
    db_group.description = group.description
    db.commit()
    db.refresh(db_group)
    return db_group

# Delete a study group (DELETE)
@router.delete("/std/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(database.StudyGroup).filter(database.StudyGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.delete(db_group)
    db.commit()
    return {"message": "Group deleted successfully"}
