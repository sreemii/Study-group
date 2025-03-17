from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(tags=["Resources"])

#Add a Resource to a Study Group
@router.post("/")
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    new_resource = models.Resource(group_id=resource.group_id, title=resource.title, url=resource.url)
    db.add(new_resource)
    db.commit()
    return {"message": "Resource added successfully"}

#get all the resources
@router.get("/", response_model=list[schemas.ResourceResponse])
def get_all_resources(db: Session = Depends(get_db)):
    """
    **Public Access**  
    Retrieves a list of all resources.
    """
    resources = db.query(models.Resource).all()
    return resources


#update the resources
@router.put("/{resource_id}", response_model=schemas.ResourceUpdate)
def update_resource(resource_id: int, resource_update: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Update only the provided fields
    update_data = resource_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resource, key, value)
    
    db.commit()
    db.refresh(resource)
    return resource
