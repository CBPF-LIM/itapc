import inspect
from flask import Blueprint, request, jsonify, render_template, redirect, current_app, url_for

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
  rel_path = caller_file.split('/routes/')[-1].strip('.py')
  return f'{rel_path}/{name}.html'


# TODO
# from flasktools import render (in every route)
# remove: TEMPLATE_BASE (not needed)
# convert all html to remove %content block%
