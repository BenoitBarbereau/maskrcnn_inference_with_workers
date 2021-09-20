# maskrcnn_inference_with_workers


# I. Install

git clone 


From my google drive download weights and mrcnn model 
https://drive.google.com/drive/folders/1E9O_j9b4ph7DpEUBI7DfQUcGVwyaVIWP?usp=sharing

Copy/paste the mask_rcnn_coco.h5 files into .app/utils/maskrcnn

# II. Webapp inference 

## STEP 1

Set up a virtual environment and install dependencies

python3 -m venv --system-site-packages ./env

source ./env/bin/activate

pip install --upgrade pip

pip install -r requirements.txt


## STEP 2 

Install and launch REDIS on a terminal

 ./run-redis.sh

## STEP 3 

Run celery on an other terminal side by side with redis

env/bin/celery worker -A app.celery --loglevel=info --pool gevent --concurrency=1

## STEP 4

run flower to monitor worker queue on your favorite browser

source env/bin/activate

flower -A app.celery --port=5555

reach the webapp on  http://localhost:5555/

## STEP 5

then run the application on an other terminal

source env/bin/activate

python run.py


## STEP 6

On your favorite web browser reach 127.0.0.1:5001

Select a folder containing images and maskrnn will be running with workers on the background making inference in a row without freezing the webapp

just be patient

