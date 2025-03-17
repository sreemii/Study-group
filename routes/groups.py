from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from core.security import get_current_user

router = APIRouter(tags=["Groups"])

# Dependency to Check Admin Access
def admin_required(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user

# User joins a study group (Only one group allowed)
@router.post("/join-group", response_model=schemas.GroupMemberResponse)
def join_study_group(
    group_member: schemas.GroupMemberCreate,
    db: Session = Depends(get_db)
):
    """
    Allows any user to join a study group **without authentication**.
    - Users can **only join one group at a time**.
    - If they are already in a group, they **cannot join another**.
    """
    # Ensure the user_id is provided in the request body
    if not group_member.user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")

    # Check if the user is already in a study group
    existing_membership = db.query(models.GroupMember).filter(
        models.GroupMember.user_id == group_member.user_id
    ).first()

    if existing_membership:
        raise HTTPException(status_code=400, detail="User can only join one study group.")

    #Add the user to the group
    new_membership = models.GroupMember(user_id=group_member.user_id, group_id=group_member.group_id)
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)

    return new_membership


#User leaves a study group
@router.delete("/leave-group/{user_id}")
def leave_group(user_id: int, db: Session = Depends(get_db)):
    """
    Allows any user to leave their current study group without authentication.
    - If the user is not in a group, returns an error.
    """
    group_member = db.query(models.GroupMember).filter(
        models.GroupMember.user_id == user_id
    ).first()

    if not group_member:
        raise HTTPException(status_code=404, detail="User is not in any study group.")

    db.delete(group_member)
    db.commit()
    return {"message": "User removed from group successfully"}

#Create a new group
@router.post("/", response_model=schemas.StudyGroupResponse, dependencies=[Depends(admin_required)])
def create_group(group: schemas.StudyGroupCreate, db: Session = Depends(get_db)):
    new_group = models.StudyGroup(name=group.name, description=group.description)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

#Get a all Groups
@router.get("/", response_model=list[schemas.StudyGroupResponse])
def get_all_groups(db: Session = Depends(get_db)):
    """
    **Public Access**  
    Retrieves a list of all study groups.
    """
    groups = db.query(models.StudyGroup).all()
    return groups

#get group by ID
@router.get("/{group_id}", response_model=schemas.StudyGroupResponse)
def get_group_by_id(group_id: int, db: Session = Depends(get_db)):
    """
    **Public Access**  
    Retrieves a study group by its ID.
    """
    group = db.query(models.StudyGroup).filter(models.StudyGroup.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Study group not found")

    return group



# Delete a Study Group (Admin Only)
@router.delete("/{group_id}", dependencies=[Depends(admin_required)])
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """
    **Admin Access Required**  
    Deletes a study group by its ID.  
    - Only admins can delete groups.
    """
    group = db.query(models.StudyGroup).filter(models.StudyGroup.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}
