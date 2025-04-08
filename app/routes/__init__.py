from app.routes.view.root import bp as view_root_blueprint
from app.routes.view.api import bp as view_api_blueprint
from app.routes.view.table import bp as view_table_blueprint
from app.routes.view.chart import bp as view_chart_blueprint
from app.routes.view.logs import bp as view_logs_blueprint
from app.routes.view.tools import bp as view_tools_blueprint
from app.routes.view.settings import bp as view_settings_blueprint

from app.routes.api import bp as api_blueprint

def draw_routes_for(app):
    app.register_blueprint(view_root_blueprint, url_prefix='/')
    app.register_blueprint(view_api_blueprint, url_prefix='/view/api')
    app.register_blueprint(view_table_blueprint, url_prefix='/view/table')
    app.register_blueprint(view_chart_blueprint, url_prefix='/view/chart')
    app.register_blueprint(view_logs_blueprint, url_prefix='/view/logs')
    app.register_blueprint(view_tools_blueprint, url_prefix='/view/tools')
    app.register_blueprint(view_settings_blueprint, url_prefix='/view/settings')

    app.register_blueprint(api_blueprint, url_prefix='/api')
