import csv
import io
from flask import jsonify, Response
from app.models import Experiment, Data
from tools.flasktools import *

bp = auto_blueprint()

@bp.route('/experiments/<int:id>/refresh/<int:index>')
def refresh(id, index):
    experiment = Experiment.get_or_none(Experiment.id == id)

    query = experiment.data.select().where(Data.id >= index)
    total = query.count()
    offset = max(0, total - 100)
    rows = query.offset(offset)

    def row(d):
        return { "id": d.id,
                 "row": d.cols,
                 "meta": { "t0": d.t0,
                           "t1": d.t1,
                           "device": d.device.name,
                           "created_at": d.created_at } }

    rows_payload = [row(d) for d in rows ]
    data = {'response': 'success', 'type': 'GET', 'rows': rows_payload, 'header': experiment.header}

    return jsonify(data)

@bp.route('/experiments/<int:id>/download')
def download(id):
    experiment = Experiment.get_or_none(Experiment.id == id)
    if not experiment:
        return "Experiment not found", 404

    # Prepare data
    data = experiment.data.select()
    header = experiment.header
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
