#!/usr/bin/env python3
from flask import render_template
from flask import abort
from flask import jsonify
from flask import Response
from flask import request
from flask_cors import CORS
from flask import Flask
from scripts.mist.mist import name_nodes,prep,Node,Site

app = Flask(__name__)
CORS(app, support_credentials=True)  # CORS


def displayObjs(objList):
	"""Prepair objList given for returning in the request
	
	Arguments:
		objList {} -- list of objects
	"""
	objDictList = []
	if isinstance(objList, list):
		for obj in objList:
			if isinstance(obj, Node):
				objDictList.append(vars(obj))
			elif isinstance(obj, Site):
				objDictList.append(vars(obj))
			else:
				objDictList.append(obj)
	else:
		if isinstance(objList, Node):
			objDictList.append(vars(objList))
		elif isinstance(objList, Site):
			objDictList.append(vars(objList))
		else:
			objDictList.append(objList)
	return objDictList

@app.before_first_request
def dothisfirst():
	print("API is ready")


@app.route('/', methods=['GET'])
def home():
	return render_template("index.html")


@app.route('/namenodes', methods=['GET'])
def namenodes():
    nodeJSON = [{"name": "AP0001", "mac": "de:ad:be:ef:00:01"}]
    site, nodes = prep(nodeJSON)
    # succcesses, failed = name_nodes(site, nodes)
    return jsonify({"site": displayObjs(
        site), "nodes": displayObjs(
        nodes)})


if __name__ == '__main__':
    app.run(debug=True)
    
