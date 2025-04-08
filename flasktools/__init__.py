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

def action_for(relative_path, *args, **kwargs):
    if not relative_path.startswith('.'):
        return url_for(relative_path, *args, **kwargs)

    # Get current endpoint like 'app_routes_view_table.index'
    current_endpoint = request.endpoint

    # Strip to get the "namespace" prefix: 'app_routes_view_table'
    base = current_endpoint.rsplit('.', 1)[0]

    # Build full endpoint name: 'app_routes_view_table.create'
    full_endpoint = f"{base}.{relative_path[1:]}"

    return url_for(full_endpoint, *args, **kwargs)


# Private methods

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
