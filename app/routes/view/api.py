import os
from flask import Blueprint, jsonify, current_app
from ita.models import Data

BLUEPRINT = 'view_api'
bp = Blueprint(BLUEPRINT, __name__)

@bp.route('/experiments/<int:id>/refresh/<int:index>')
def refresh(id, index):
    rows = Data.select().where(Data.id >= index)
    cols = [ {"id": d.id, "cols": d.cols} for d in rows]
    data = {'response': 'success', 'type': 'GET', 'cols': cols}

    if index == 0:
        data['header'] = rows.first().experiment.header

    return jsonify(data)
