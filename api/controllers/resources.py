from sqlalchemy.orm import Session
from ..models.resources import resources
from ..schemas.resources import resourcesSchema

def create_resource(db: Session, request: resourcesSchema):
    new_resource = resources(**request.dict())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

def get_all_resources(db: Session):
    return db.query(resources).all()

def get_resource_by_id(db: Session, resource_id: int):
    return db.query(resources).filter(resources.resource_id == resource_id).first()

def update_resource(db: Session, resource_id: int, request: resourcesSchema):
    resource = db.query(resources).filter(resources.resource_id == resource_id).first()
    if resource:
        for key, value in request.dict().items():
            setattr(resource, key, value)
        db.commit()
        db.refresh(resource)
    return resource

def delete_resource(db: Session, resource_id: int):
    resource = db.query(resources).filter(resources.resource_id == resource_id).first()
    if resource:
        db.delete(resource)
        db.commit()
    return resource
