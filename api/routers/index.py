from . import order_details,  resources
from . import orders, users, menu, review, promotion, payment, revenue


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu.router)
    app.include_router(users.router)
    app.include_router(menu.router)
    app.include_router(users.router)
    app.include_router(review.router)
    app.include_router(promotion.router)
    app.include_router(payment.router)
    app.include_router(resources.router)
    app.include_router(revenue.router)
