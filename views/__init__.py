# views/__init__.py
from .user_views import user_blueprint
from .admin_views import admin_blueprint
from .merchant_views import merchant_blueprint

def register_blueprints(app):
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(merchant_blueprint)
