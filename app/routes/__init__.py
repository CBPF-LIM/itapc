from app.routes.view.api import bp as view_api_blueprint
from app.routes.view.table import bp as view_table_blueprint
from app.routes.api import bp as api_blueprint
from app.routes.root import bp as root_blueprint

def draw_routes_for(app):
    app.register_blueprint(root_blueprint, url_prefix='/')
    app.register_blueprint(api_blueprint, url_prefix='/ita/exec')
    app.register_blueprint(view_api_blueprint, url_prefix='/ita/view/api')
    app.register_blueprint(view_table_blueprint, url_prefix='/ita/view/table')
