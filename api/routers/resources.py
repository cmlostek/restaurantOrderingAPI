from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers.resources import (
    create_resource,
    get_all_resources,
    get_resource_by_id,
    update_resource,
    delete_resource,
)
from ..schemas.resources import resourcesSchema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/resources",
    tags=["resources"]
)

@router.post("/", response_model=resourcesSchema)
def create_new_resource(request: resourcesSchema, db: Session = Depends(get_db)):
    return create_resource(db, request)

@router.get("/", response_model=list[resourcesSchema])
def read_all_resources(db: Session = Depends(get_db)):
    return get_all_resources(db)

@router.get("/{resource_id}", response_model=resourcesSchema)
def read_resource_by_id(resource_id: int, db: Session = Depends(get_db)):
    resource = get_resource_by_id(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/{resource_id}", response_model=resourcesSchema)
def update_existing_resource(resource_id: int, request: resourcesSchema, db: Session = Depends(get_db)):
    resource = update_resource(db, resource_id, request)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.delete("/{resource_id}", response_model=resourcesSchema)
def delete_existing_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = delete_resource(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource