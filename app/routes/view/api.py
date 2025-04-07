import os
import csv
import json
import io
from flask import Blueprint, jsonify, current_app, Response
from ita.models import Experiment, Data

BLUEPRINT = 'view_api'
bp = Blueprint(BLUEPRINT, __name__)

@bp.route('/experiments/<int:id>/refresh/<int:index>')
def refresh(id, index):
    experiment = Experiment.get_or_none(Experiment.id == id)

    query = experiment.data.select().where(Data.id >= index)
    total = query.count()
    offset = max(0, total - 100)
    rows = query.offset(offset)

    cols = [ {"id": d.id, "cols": d.cols} for d in rows]
    data = {'response': 'success', 'type': 'GET', 'cols': cols}
    data['header'] = json.loads(experiment.header)

    return jsonify(data)

@bp.route('/experiments/<int:id>/download')
def download(id):
    experiment = Experiment.get_or_none(Experiment.id == id)
    if not experiment:
        return "Experiment not found", 404

    # Prepare data
    data = experiment.data.select()
    header = json.loads(experiment.header)
    cols = [ {"id": d.id, "cols": d.cols} for d in data ]

    # Create CSV in-memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header: "ID" + headers
    writer.writerow(["ID"] + header)

    # Write each row: d.id + d.cols
    for row in cols:
        writer.writerow([row["id"]] + row["cols"])

    # Return as a file download
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=experiment_{id}.csv"}
    )
