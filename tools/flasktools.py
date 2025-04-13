import inspect
from flask import Blueprint, request, render_template,current_app, url_for, g

# Public methods

def emitter(event, data):
    return current_app.socketio.emit(event, data)

def render(name, *args, **kwargs):
  return render_template(_layout(kwargs), body=_page(name), *args, **kwargs)

def auto_blueprint():
     # Get caller's frame
    caller_frame = inspect.stack()[1].frame

    # Grab the caller module's __name__
    caller__name__ = caller_frame.f_globals['__name__']

    # Replace dots to avoid conflicts
    blueprint_name = caller__name__.replace('.', '/')

    return Blueprint(blueprint_name, caller__name__)

# Wrapper for Flask's url_for, but with short "dot" notation.
# drop to normal url_for if the endpoint is not in dot notation
def action_for(endpoint, external=False, *args, **kwargs):
    return url_for(_resolve_endpoint(endpoint), _external=external, *args, **kwargs)

# Relative alternative of action_for
def action_path(endpoint, *args, **kwargs):
    return url_for(_resolve_endpoint(endpoint), *args, **kwargs)

# Absolute alternative of action_for
def action_url(endpoint, *args, **kwargs):
    return url_for(_resolve_endpoint(endpoint), _external=True, *args, **kwargs)


# Private methods

def _resolve_endpoint(dot_path):
    if not dot_path.startswith('.'):
        return dot_path
    base = request.endpoint.rsplit('.', 1)[0]
    return f"{base}.{dot_path[1:]}"

def _layout(kwargs):
  name = kwargs.pop('layout', 'application')
  return f'layouts/{name}.html'

def _page(name):
  frame = inspect.stack()[2]  # page is called from render[1]. Render is called from the route[2]
  caller_file = frame.filename
  rel_path = caller_file.split('/views/')[-1].strip('.py')
  return f'{rel_path}/{name}.html'

class Params:
    def __init__(self):
        self.data = {}
        self._load()

    def _load(self):
        # Merge GET params
        for key in request.args:
            values = request.args.getlist(key)
            self.data[key] = values if len(values) > 1 else values[0]

        # Merge POST form params
        for key in request.form:
            values = request.form.getlist(key)
            self.data[key] = values if len(values) > 1 else values[0]

        # Merge JSON body (if present and valid)
        try:
            json_data = request.get_json(silent=True)
            if isinstance(json_data, dict):
                self.data.update(json_data)
        except Exception:
            pass  # Safely ignore invalid JSON

    def __getitem__(self, key):
        return self.data.get(key, None)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def to_dict(self):
        return dict(self.data)

    def permit(self, *fields):
        return {k: v for k, v in self.data.items() if k in fields}

def params():
    if not hasattr(g, '_params'):
        g._params = Params()
    return g._params

def register_flasktools_helpers(app):
    @app.context_processor
    def expose_helpers():
        return dict(
            action_for=action_for,
            action_path=action_path,
            action_url=action_url,
            params=params
        )

def _rule_hash(rule):
    view_action = rule.endpoint.split('.')
    view = view_action[0]
    action = view_action[-1]

    if view == action:
        view = ''

    methods = set(rule.methods) & {'GET', 'POST', 'PUT', 'DELETE', 'PATCH'}

    return {
        'methods': ','.join(sorted(methods)),
        'endpoint': rule.rule,
        'view': rule.endpoint.replace('.', '#').replace('/', '.'),
        }

def get_routes(app):
    return [_rule_hash(rule) for rule in app.url_map.iter_rules()]
