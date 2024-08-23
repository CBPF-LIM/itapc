from flask import Flask, request, jsonify
import os
import ita
from app import response
from tools.shortcuts import b

app = Flask(__name__)

@app.route('/ita/exec', methods=['POST'])
@app.route('/ita/exec/', methods=['POST'])
def doPost():
    data = ita.processPost(request.json)
    return response.process(data)

@app.route('/ita/exec', methods=['GET'])
@app.route('/ita/exec/', methods=['GET'])
def doGet():
    q = request.args.to_dict()
    data = ita.processGet(q)
    return response.process(data)

def main():
    port = os.getenv('ITA_PORT', 5000)
    debug = os.getenv('ITA_DEBUG', False)
    app.run(port=port, debug=debug)

if __name__ == '__main__':
    main()
