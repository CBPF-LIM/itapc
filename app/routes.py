from importlib import import_module
from tools.shortcuts import b
import yaml

def draw_routes_for(app, prefix='', import_prefix=''):
    blueprint_map = load_routes(app)
    recursive_draw(app, blueprint_map, prefix, import_prefix)

def recursive_draw(app, blueprint_map, prefix='', import_prefix=''):
    for key, value in blueprint_map.items():
        if isinstance(value, dict):
            # Recurse into nested group
            new_prefix = f"{prefix}/{key}".strip('/')
            new_import_prefix = f"{import_prefix}.{key}" if import_prefix else key
            recursive_draw(app, value, new_prefix, new_import_prefix)
        else:
            # Build the full module path
            module_path = f"app.views.{import_prefix}.{key}" if import_prefix else f"app.views.{key}"

            if value.startswith('/'):
                url_prefix = value
            else:
                url_prefix = f"/{prefix}/{value}".replace('//', '/')

            module = import_module(module_path)
            blueprint = getattr(module, 'bp')
            app.register_blueprint(blueprint, url_prefix=url_prefix)

def load_routes(app):
    with open('app/routes.yml', 'r') as file:
        routes = yaml.safe_load(file)

    return routes
