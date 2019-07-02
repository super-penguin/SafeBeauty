from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import cv2
import json
import numpy as np
import tensorflow as tf
# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util
import collections
# Flask utils
from flask import Flask, redirect, url_for, request, render_template, send_file
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import pandas as pd
import json

# Define a flask app
app = Flask(__name__, static_url_path='/static')

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
# sys.path.append(os.getcwd())

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'
# IMAGE_NAME = '/uploads/demo_03.jpg'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Path to image
# PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)

# Number of classes the object detector can identify
NUM_CLASSES = 7

# Load the label map.

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load your trained model
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

print('Model loaded. Check http://127.0.0.1:5000/')


def object_detection(path, sess):
    # image = cv2.imread(PATH_TO_IMAGE)
    # image_expanded = np.expand_dims(image, axis=0)
    # Perform the actual detection by running the model with the image as input
    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    image = cv2.imread(path)
    image_expanded = np.expand_dims(image, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.80)

    cv2.imwrite('static/results.jpg', image)

    NAME = []
    threshold = 0.8
    for index, value in enumerate(classes[0]):
        if scores[0, index] > threshold:
            NAME.append((category_index.get(value)).get('name'))


    data = pd.read_csv("LookUp.csv")

    Output = {}
    if not NAME:
        Output['Title'] = 'Your skin care cabinet is SAFE.'
    else:
        Output['Title'] = ' WARNING: avoid using the detected products!'
        Output['Product'] = []
        for name in NAME:
            Output['Product'].append({'Name': data.loc[data['name'] == name]['BrandName'].values[0],
            'Ingredient': data.loc[data['name'] == name]['Ingredient'].values[0],
            'Info': data.loc[data['name'] == name]['Info'].values[0]})

        Output_json = json.dumps(Output)
        return Output_json

# print (object_detection(IMAGE_NAME, sess))

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        result = object_detection(file_path, sess)
        return result
    return None

if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
