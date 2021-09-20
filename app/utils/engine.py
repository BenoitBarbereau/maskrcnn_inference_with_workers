
from mrcnn import model
from app.utils.config_maskrcnn import config
from app.utils import custom_visualize
from flask import Flask, request, redirect, jsonify
from mrcnn.model import MaskRCNN
import skimage
import colorsys
import tensorflow as tf
import mrcnn.model as modellib
import numpy as np
import os 
from PIL import Image

class ModelInference():
    def __init__(self,config, mode=None, model=None, graph=None):
        self.config = config
        if mode == "worker":
            self.model = model
            self.graph = graph
        else:
            self.model = modellib.MaskRCNN(
                mode="inference", config=self.config, model_dir=self.config.COCO_MODEL_PATH)
            self.model.load_weights(self.config.MODEL_DIR, by_name=True)
            self.graph = tf.get_default_graph()
        self.mode = mode    
        self.image = np.zeros((2, 3), dtype = int)
        self.masked_image = np.zeros((2, 3), dtype=int)
        self.result = {} 


    def check_convert_image(self, image):
        try:
            #image = Image.open(image)
            print(type(image))
            img = np.asarray(image)
            return img 
        except Exception as e:
            return e
            

    def inference(self, image):
        with self.graph.as_default():
            self.result = self.model.detect([image], verbose=0)[0]
            self.masked_image = custom_visualize.custom_display_instances(image,
                                                                    boxes=self.result['rois'], 
                                                                    masks=self.result['masks'], 
                                                                    class_ids=self.result['class_ids'],
                                                                    class_names=self.config.CLASS_NAMES,
                                                                    scores=self.result['scores']
                                                                    )
        return self.result, self.masked_image

    def responsify(self, r , masked_image):
        '''
        last step, this function build response to return
        '''
        boxes = r['rois']
        masks = r['masks']
        ids = r['class_ids']
        scores = r['scores']
        names = self.config.CLASS_NAMES
        n_instances = boxes.shape[0]
        if n_instances:
            response = {
                "code": 200,
                "data": r,
                "masked_image": masked_image
            }
            return response
        else:
            print(ids)
            response = {
                "code": 204,
                "errors": "no instances found"
            }
            return response


    def run_inference(self, image):
        try:
            img = self.check_convert_image(image)
            r, masked_image = self.inference(img)
            response = self.responsify(r, masked_image)
            return response
        except Exception as e:
            return {
                "code": 500,
                "errors": e
                    }


inference_mrcnn = ModelInference(config)
