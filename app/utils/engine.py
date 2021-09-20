
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

class Foamtastic():
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


    def concat(self, boxes,masks,ids,scores,names): 
        '''
        Concat all information about one object detected
        '''
        dic_detection ={}
        i = 0 
        for box in boxes:
            x1, y1, x2, y2 = boxes[i]
            height = x2 - x1
            width = y2 - y1
            x_center_box = x1 + ((x2-x1)/2)
            y_center_box = y1 + ((y2-y1)/2)
            surface = width * height
            dic_detection[i] = (x1, y1, x2, y2, width, height, surface, x_center_box, y_center_box, ids[i], names[ids[i]], scores[i],masks[i])
            i += 1
        return dic_detection

    def get_main_object(self, dic,ids=1):
        '''
        here the function try to detect main object (tube) amid all object with the same class
        '''
        #tube == objet détecté class tube
        tmp = {}
        sum_surface = []
        n = 0
        for key, value in dic.items():
            if value[9] == ids :
                tmp[key]= value
                sum_surface.append(value[6])
        # critère pour garder les plus gros objets 
        # moyenne surface du premier quantile (tri + grd au petit)
        taille = round(len(sum_surface)*0.51)
        surface_sorted = sorted(sum_surface, reverse = True)
        surface_quantile = surface_sorted[:taille]
        criteria = np.mean(surface_quantile[:taille])*0.70
        return tmp , criteria    

    def sort_tube(self, dic, criteria_mean):
        '''
        sort object from left to right
        '''
        object_sorted = {}
        for k, v in sorted(dic.items(), key=lambda e: e[1][8]):
            if v[6] > criteria_mean:
                object_sorted[k] = v
        return object_sorted


    def convertion_pxl_cm(self, m, width_pxl, width_cm =  2.5 ):
        width_cm = self.config.WIDTH_TUBE
        return (width_cm * m) / width_pxl

    
    def convert_dic_list_to_dic(self, dic):
        dic_tube = {}
        keys = ("x1", "y1", "x2", "y2", "width", "height", "surface", "x_center_box",
                "y_center_box", "ids", "class", "scores","mask")
        for k, v in dic.items():
            tmp = {}
            n = 0
            for element in keys:
                tmp[element] = v[n]
                n +=1
            dic_tube[k] = tmp
        return dic_tube


    def is_in_tube(self, dic_objet, dic_all):
        '''
        Detect objet inside an object. If the centerpoint of a sub object is detected inside a main (larger object)
        means it belong to the main object. 
        '''
        foam = {}
        list_objet = dic_objet.keys()
        i = 1 
        for k,v in dic_objet.items():
            data = {}
            data[f"{v['class']}_{k}"] = v
            for ky,voodoo in dic_all.items():
                if v['x1']< voodoo['x_center_box'] < v['x2'] and v['y1']< voodoo['y_center_box'] < v['y2']:
                    if voodoo['ids']== 3:
                        data[f"{voodoo['class']}_{ky}"] = voodoo
            foam["range_"+ str(i)] = data
            i +=1
        return foam

    def display_img_tube(self, dictionnary, image):
        i = 1
        response = []
        for k, v in dictionnary.items():
            for key, value in v.items():
                x1 = value["x1"]
                y1 = value["y1"]
                x2 = value["x2"]
                y2 = value["y2"]
                height = value["height"]
                crop_img = image[x1:x2, y1:y2]
                if value["ids"] == 1:
                    width_tube = value["width"]
                    x = self.convertion_pxl_cm(height, width_tube)
                    print(f"tube n°{i} d'une hauteur de {x} cm")
                    response.append(f"tube n°{i} d'une hauteur de {x} cm")
                else:
                    x = self.convertion_pxl_cm(height, width_tube)
                    print(f"la mousse dans le tube n°{i} a une hauteur de {x} cm")
                    print(x1,x2, y1,y2)
                    response.append(f"la mousse dans le tube n°{i} a une hauteur de {x} cm")
                #plt.figure(figsize=(10,10))
                #plt.imshow(crop_img)
            i+=1 
        return response
    

    def response_foamtastic(self, r , masked_image):
        '''
        last step, this function build response to return
        '''
        boxes = r['rois']
        masks = r['masks']
        ids = r['class_ids']
        scores = r['scores']
        names = self.config.CLASS_NAMES
        n_instances = boxes.shape[0]
        # if not n_instances:
        if 1 in ids:
            # if there is class tube (=1) in prediction list of class
            assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]
            dic = self.concat(boxes, masks, ids, scores, names)
            dic_main_object, criteria = self.get_main_object(dic)
            object_sorted = self.sort_tube(dic_main_object, criteria)
            les_tubes = self.convert_dic_list_to_dic(object_sorted)
            tout = self.convert_dic_list_to_dic(dic)
            les_tube_et_mousse = self.is_in_tube(les_tubes, tout)
            # response = self.display_img_tube(les_tube_et_mousse, image)
            response = {
                "code": 200,
                "data": les_tube_et_mousse,
                "masked_image": masked_image
            }
            return response
        else:
            print(ids)
            response = {
                "code": 204,
                "errors": "no instance of tube found within the image"
            }
            return response


    def run_inference(self, image):
        try:
            img = self.check_convert_image(image)
            r, masked_image = self.inference(img)
            response = self.response_foamtastic(r, masked_image)
            return response
        except Exception as e:
            return {
                "code": 500,
                "errors": e
                    }


foamtastic = Foamtastic(config)
