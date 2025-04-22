from . import orders, users, menu, resources


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(menu.router)
    app.include_router(users.router)
    app.include_router(resources.router)
