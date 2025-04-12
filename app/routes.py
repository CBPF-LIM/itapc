from app.views.view.root import bp as view_root_blueprint
from app.views.view.api import bp as view_api_blueprint
from app.views.view.logs import bp as view_logs_blueprint
from app.views.view.settings import bp as view_settings_blueprint
from app.views.view.experiments import bp as view_experiments_blueprint

from app.views.api import bp as api_blueprint

def draw_routes_for(app):
    app.register_blueprint(view_root_blueprint, url_prefix='/')
    app.register_blueprint(view_api_blueprint, url_prefix='/view/api')
    app.register_blueprint(view_logs_blueprint, url_prefix='/view/logs')
    app.register_blueprint(view_settings_blueprint, url_prefix='/view/settings')
    app.register_blueprint(view_experiments_blueprint, url_prefix='/view/experiments')

    app.register_blueprint(api_blueprint, url_prefix='/api')
