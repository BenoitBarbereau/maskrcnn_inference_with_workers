

#App
import config # Watch out flask config
from flask import current_app

#AI
from mrcnn.model import MaskRCNN
import mrcnn.model as modellib
from app.utils.config_maskrcnn import config as InferenceConfig  # watch out AI config
from app.utils.engine import ModelInference
from keras import backend as K
import tensorflow as tf

#Celery
from celery.signals import worker_init, worker_process_init, celeryd_init
from celery.concurrency import asynpool
from celery.utils.log import get_task_logger
from celery import Celery

#Image
import numpy as np
from numpyencoder import NumpyEncoder
import cv2
import base64
import json
from io import BytesIO
from PIL import Image


asynpool.PROC_ALIVE_TIMEOUT = 100.0 #set this long enough
app = current_app
logger = get_task_logger(__name__)
celery = Celery(app.name, backend=config.CELERY_RESULT_BACKEND,
                broker=config.CELERY_BROKER_URL)
celery.conf.update(app.config)

def image_PIL_to_str(image_pil):
    buffered = BytesIO()
    image_pil.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
    return img_str


def image_str_to_cv(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(BytesIO(imgdata))
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    return img_cv


def image_cv_to_str(image_cv):
    #img_str = cv2.imencode('.jpg', image_cv)[1].tostring()
    retval, buffer = cv2.imencode('.jpg', image_cv)
    jpg_as_text = base64.b64encode(buffer).decode('ascii')
    return jpg_as_text


@celery.task(bind=True)
def task_mrcnn(self, base64_string):
    print("Inference")
    self.update_state(state='PROGRESS',
                      meta={'current': 33, 'total': 100,
                            'status': 'Intialisation'})
    try:
        image = image_str_to_cv(base64_string)
        K.clear_session()
        model = modellib.MaskRCNN(
            mode="inference", config=InferenceConfig, model_dir=InferenceConfig.COCO_MODEL_PATH)
        logger.info('Inference for worker: modellib.MaskRCNN')
        model.load_weights(InferenceConfig.MODEL_DIR, by_name=True)
        logger.info('Inference for worker: modellib.MaskRCNN weights loaded')
        GRAPH = tf.get_default_graph()
        with GRAPH.as_default():
            logger.info(
                'Inference for worker: inference in progress... ')
            mrcnn = ModelInference(InferenceConfig, "worker", model, GRAPH)
            result = mrcnn.run_inference(image)
            logger.info(f'model for worker: inference done, code --> {result["code"]}')
        K.clear_session()
        if result["code"] == 200: 
            img = image_PIL_to_str(result['masked_image'])
            result['masked_image'] = img
            resp = json.dumps(result, cls=NumpyEncoder)
            logger.info(result['data'])
            return {'current': 100, 'total': 100, 'status': 'Task completed!',
                    'result': resp}
        else:
            resp = json.dumps(result, cls=NumpyEncoder)
            return {'current': 100, 'total': 100, 'status': 'Task completed!',
                    'result': resp }
    except Exception as e:
        logger.info(e)
        print(e)
        return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': str(e)}






