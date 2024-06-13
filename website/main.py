from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import json
import requests
import pymongo
import subprocess
import os
import time
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin




app = Flask(__name__)
CORS(app, support_credentials=True)


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["newsdata"]
mycol = mydb["news"]








@app.route("/",methods=["GET","POST"])
@cross_origin(supports_credentials=True)
def main():
	data = []
	for x in mycol.find():
		if x['show'] == 1:
			data.append(x)
	return render_template("index.html",data=data)

@app.route("/news",methods=["GET","POST"])
@cross_origin(supports_credentials=True)
def news():
	id__ = request.args.get('id')
	x = mycol.find_one({'_id':ObjectId(id__)})
	return render_template("post.html",data=x)








app.run(debug = True, threaded=True, host='0.0.0.0', port=5001)