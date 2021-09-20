# Webapp maskrcnn inference Multiprocessing

# Abstract
This is a flask webapplication. The interface on the browser is used to send a bunch of images and display inferences of maskrcnn as a result.

The backend is built with python (flask, celery, tensorflow-keras, opencv) and redis for queuing tasks.

here the result: 

[](./doc/result.png)
![image info](./doc/result.png)



The maskrcnn coco is pre trained to recognize 81 classes :

['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 
'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 
'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 
'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 
'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 
'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 
'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 
'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 
'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 
'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 
'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 
'teddy bear', 'hair drier', 'toothbrush']

# I. Install

git clone https://github.com/BenoitBarbereau/maskrcnn_inference_with_workers.git


From matterport github download weights and mrcnn coco model 
https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5

Copy/paste the mask_rcnn_coco.h5 files into ./app/utils/maskrcnn

Set up a virtual environment and install dependencies

python3 -m venv --system-site-packages ./env

source ./env/bin/activate

pip install --upgrade pip

pip install -r requirements.txt


# II. Webapp inference 


### step 1 

Install and launch REDIS on a terminal

 ./run-redis.sh

### step 2

Run celery on an other terminal side by side with redis

env/bin/celery worker -A app.celery --loglevel=info --pool gevent --concurrency=1

### step 3 

run flower to monitor worker queue on your favorite browser

source env/bin/activate

flower -A app.celery --port=5555

reach flower webapp on  http://localhost:5555/

### step 4

then run the application on an other terminal

source env/bin/activate

python run.py


### step 5

On your favorite web browser reach 127.0.0.1:5001

Select a folder containing images  ( ./Images_test )  and maskrnn will be running inferences in a row with workers on the background without freezing the webapp

just be patient

