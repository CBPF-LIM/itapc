from app.routes.view import bp as view_blueprint
from app.routes.api import bp as api_blueprint
from app.routes.root import bp as root_blueprint

def draw_routes_for(app):
    app.register_blueprint(root_blueprint, url_prefix='/')
    app.register_blueprint(api_blueprint, url_prefix='/ita/exec')
    app.register_blueprint(view_blueprint, url_prefix='/ita/view')
