from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from core.security import get_current_user 

router = APIRouter(tags=["Users"])

# Dependency to Check Admin Access
def admin_required(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user

# Get All Users (Admin Only)
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    """
    **Admin Access Required**  
    Retrieves a list of all users.
    """
    return db.query(models.User).all()

# Get User by ID (User & Admin)
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    **User or Admin Access**  
    - Users can only access their **own profile**.  
    - Admins can view **any user profile**.
    """
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied.")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update User Profile (User Only)
@router.put("/update-profile", response_model=schemas.UserResponse)
def update_profile(
    user_update: schemas.UserUpdate, db: Session = Depends(get_db)
):
    """
    **User Access Only**  
    - Users can **update their own profile**.
    """
    user = db.query(models.User).filter(models.User.email == user_update.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name is not None:  
        user.name = user_update.name  
    if user_update.email is not None:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return user



# Promote User to Admin (Admin Only)
@router.put("/promote/{user_id}")
def promote_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)  # ✅ Ensure it uses models.User
):
    """
    **Admin Access Required**  
    - Only an **admin** can promote a user to admin.
    """

    # ✅ Ensure only admins can promote users
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can promote users.")

    # ✅ Find the user to be promoted
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Ensure the user is not already an admin
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="User is already an admin.")

    # ✅ Promote the user
    user.role = "admin"
    db.commit()
    db.refresh(user)

    return {"message": f"User {user.email} has been promoted to admin."}




# Delete User (Admin Only)
@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    **Admin Access Required**  
    - Allows an **admin to delete a user and all related data**.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete related data before deleting the user
    db.query(models.StudyGroup).filter(models.StudyGroup.owner_id == user_id).delete(synchronize_session=False)
    db.query(models.StudySession).filter(models.StudySession.created_by == user_id).delete(synchronize_session=False)
    db.query(models.Resource).filter(models.Resource.uploaded_by == user_id).delete(synchronize_session=False)
    db.query(models.GroupMember).filter(models.GroupMember.user_id == user_id).delete(synchronize_session=False)

    # Now, delete the user
    db.delete(user)
    db.commit()

    return {"message": "User and all related data deleted successfully"}
