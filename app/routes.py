
import config
import json
import os
from flask import Flask, url_for, render_template, request, flash, redirect, jsonify, current_app, Blueprint
from werkzeug.utils import secure_filename
import base64
import cv2
import time
import base64
import io
from PIL import Image
import numpy as np
from app.workers.workers_foamtastic import task_foamtastic

app = current_app



@app.route("/", methods=["GET", "POST"])
def index():
    print(f"running on {request.host}")
    #if request.method == 'GET':
    return render_template("index.html")
    #return redirect(url_for('index'))


#POUR UN DOSSIER D'IMAGE
@app.route("/foldertask", methods=["POST"])
def upload_folder():
    data_photos = request.files.getlist('photoFileFolder')
    lst = []
    for img in data_photos:
        try:
            base64_string = base64.b64encode(img.read()).decode('ascii')
            task = task_foamtastic.delay(base64_string)
            lst.append(task.id.strip())
        except Exception as e:
            return e
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id), 'task_id': lst }


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = task_foamtastic.AsyncResult(task_id)
    print(task.state)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0.02,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current'),
            'total': task.info.get('total'),
            'status': task.info.get('status')
        }
        if 'result' in task.info:
            worker_response = task.info['result']
            resp = json.loads(worker_response)
            if int(resp['code']) == 200:
                image = resp['masked_image']
                data_inference = resp['data']
                response['image'] = "data:image/png;base64," + image
                response['data_inference'] = data_inference
            else: 
                #response['data_inference'] = resp['errors']
                response = {
                    'state': task.state,
                    'current': 1,
                    'total': 1,
                    # this is the exception raised
                    'status': str(resp['errors']),
                }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


