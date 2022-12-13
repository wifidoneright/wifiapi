#!/usr/bin/env python3
import logging
from flask import render_template
from flask import abort
from flask import jsonify
from flask import Response
from flask import request
from flask_cors import CORS
from flask import Flask
from scripts.mist.mist import name_aps,prep,Node,Site,displayObjs

app = Flask(__name__)
CORS(app, support_credentials=True)  # CORS


@app.before_first_request
def dothisfirst():
	print("API is ready")


@app.route('/', methods=['GET'])
def home():
	return render_template("index.html")


# @app.route('/nameap/<id>', methods=['POST'])
# def nameaps(id):  # path Parameter example
@app.route('/nameaps', methods=['POST'])
def nameaps():
    try:
        vendor = request.args.get("vendor") # Query Parameter
        node_json = request.get_json() #Body
        site, aps = prep(node_json)
        succcesses, failed = name_aps(site, aps)
        return jsonify({"success": displayObjs(succcesses),
            "failed": displayObjs(failed)})
        return jsonify({"site": displayObjs(
            site), "aps": displayObjs(
            aps)})
    except Exception as e: #handle errors
        logging.error(e)
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
    
