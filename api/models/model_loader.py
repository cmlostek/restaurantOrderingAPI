from  . import menu, users, orders, order_details, review, payment, promotion
from ..dependencies.database import engine


def index():
    # Create all tables in the database
    menu.Base.metadata.create_all(bind=engine)
    users.Base.metadata.create_all(bind=engine)
    orders.Base.metadata.create_all(bind=engine)
    order_details.Base.metadata.create_all(bind=engine)
    review.Base.metadata.create_all(bind=engine)
    payment.Base.metadata.create_all(bind=engine)
    promotion.Base.metadata.create_all(bind=engine)

