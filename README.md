# maskrcnn_inference_with_workers



## STEP 1

Set up a virtual environment and install dependancies

python3 -m env --system-site-packages ./venv
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

run flower to monitor all above on an other terminal too

source env/bin/activate
flower -A app.celery --port=5555

## STEP 5

then run the application on an other terminal

source env/bin/activate
python run.py


## STEP 6
Go on your favorite web browser 127.0.0.1:5555

Select a folder containing images and maskrnn will be running on the background making inference in a row without freezing the app

just be patient
