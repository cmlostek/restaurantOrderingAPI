import json
from pathlib import Path
from sqlalchemy.orm import Session
from api.dependencies.database import Base, SessionLocal, engine
from api.models import users, menu, orders, order_details, payment, promotion, resources, review

# Use bcrypt directly to avoid passlib compatibility issues
try:
    import bcrypt
    import os
    
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt directly"""
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        # Hash using bcrypt with salt
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')
        
except ImportError:
    # Fallback to hashlib if bcrypt is not available
    import hashlib
    
    def hash_password(password: str) -> str:
        """Hash a password using SHA256 (fallback)"""
        return hashlib.sha256(password.encode()).hexdigest()

# json folder
DATA_PATH = Path(__file__).parent / "data"

def load_json(fname: str):
    # load json file from data folder
    return json.loads((DATA_PATH / fname).read_text())

def seed_data(db: Session):
    # dropping and recreating db
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # add users to db
    users_data = load_json("users.json")
    for u in users_data:
        # Hash the password if it's a plain password
        if 'password' in u and not u['password'].startswith('$2b$'):
            u['password'] = hash_password(u['password'])
        
        db.add(users.User(**u))
    db.commit()

    # add menu to db
    db.add_all([
        menu.menu(
            dish_id=m["dish_id"],
            dish=m["dish"],
            price=m["price"],
            calories=m["calories"],
            category=m["category"]
        ) for m in load_json("menu.json")
    ])
    db.commit()

    # add resources to db
    db.add_all([resources.resources(**r) for r in load_json("resources.json")])
    db.commit()

    # backref menu with ingredients
    for m in load_json("menu.json"):
        dish_obj = db.query(menu.menu).get(m["dish_id"])
        if dish_obj:
            ing_objs = (
                db.query(resources.resources)
                  .filter(resources.resources.resource_id.in_(m["ingredients"]))
                  .all()
            )
            dish_obj.ingredients = ing_objs
    db.commit()


    # add orders to db
    db.add_all([orders.Order(**o) for o in load_json("orders.json")])
    db.commit()

    # add promotions to db
    db.add_all([promotion.Promotion(**pr) for pr in load_json("promotions.json")])
    db.commit()

    # add payments to db
    db.add_all([payment.Payment(**p) for p in load_json("payments.json")])
    db.commit()

    # add order details to db
    db.add_all([order_details.OrderDetails(**od) for od in load_json("order_details.json")])
    db.commit()

    # add reviews to db
    db.add_all([review.Review(**rv) for rv in load_json("reviews.json")])
    db.commit()




if __name__ == "__main__":
    session = SessionLocal()
    try:
        seed_data(session)
        print("Database seeded successfully.")
    finally:
        session.close()
