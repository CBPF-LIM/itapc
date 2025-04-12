from flasktools import *

bp = auto_blueprint()

@bp.route('/', methods=['GET'])
def index():
    return render('index')
