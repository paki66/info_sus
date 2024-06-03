from flask import Flask, request, jsonify, render_template
import model
from datetime import datetime


app = Flask(__name__)


@app.route('/transakcija', methods=['POST'])
def kreiraj_transakciju():
    try:
        json_request = request.json
    except Exception as e:
        response = {"response": str(e)}
        return jsonify(response), 400

    response = model.add_transakcija(json_request)
    
    if response["response"] == "Success":    
        return jsonify({"message": 'Transakcija dodana'}), 201
    return jsonify(response), 400


@app.route('/transakcija', methods=['GET'])
def dohvati_transakcije():
    if request.args and "id" in request.args:
        transakcija_id = int(request.args.get("id"))
        response = model.get_transakcija_by_id(transakcija_id)

        if response["response"] == "Success":
            return jsonify(response["data"]), 200
        return jsonify(response), 400
    
    response = model.get_transakcije()
    if response["response"] == "Success":
        return jsonify(response), 200
    return jsonify(response), 400


#@app.route('/transakcija/pretraga', methods=['GET'])


@app.route('/transakcija', methods=['PATCH'])
def uredi_transakciju():
    try:
        json_request = request.json
    except Exception as e:
        response = {"response": str(e)}
        return jsonify(response), 400
    
    if request.args:
        transakcija_id = int(request.args.get("id"))
        response = model.patch_transakcija(transakcija_id, json_request)

        if response["response"] == "Success":
            return jsonify(response), 200
        return jsonify(response), 400
    
    response = {"response": "Nedostaje id u zahtjevu"}
    return jsonify(response), 400


@app.route('/transakcija', methods=['DELETE'])
def izbrisi_transakciju():
    if request.args:
        transakcija_id = int(request.args.get("id"))
        response = model.delete_transakcija(transakcija_id)

        if response["response"] == "Success":
            return jsonify(response), 200
        return jsonify(response), 400
    
    response = {"response": "Nedostaje id u zahtjevu"}
    return jsonify(response), 400

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
