import os
import json
from flask import Blueprint, jsonify, current_app
from ita.models import Experiment, Data

BLUEPRINT = 'view_api'
bp = Blueprint(BLUEPRINT, __name__)

@bp.route('/experiments/<int:id>/refresh/<int:index>')
def refresh(id, index):
    experiment = Experiment.get_or_none(Experiment.id == id)
    # rows = Data.select().where(Data.id >= index)

    query = experiment.data.select().where(Data.id >= index)
    total = query.count()
    offset = max(0, total - 100)
    rows = query.offset(offset)

    cols = [ {"id": d.id, "cols": d.cols} for d in rows]
    data = {'response': 'success', 'type': 'GET', 'cols': cols}
    data['header'] = json.loads(experiment.header)

    return jsonify(data)
