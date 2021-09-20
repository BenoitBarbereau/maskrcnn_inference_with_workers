

from mrcnn.config import Config
import os



class InferenceConfig(Config):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    NAME = "foamtastic"
    ROOT_DIR = os.path.abspath(".")
    COCO_MODEL_PATH = os.path.join(ROOT_DIR , 'app/utils/maskrcnn')
    MODEL_DIR = os.path.join( COCO_MODEL_PATH, "mask_rcnn_coco.h5")
    CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 
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
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = len(CLASS_NAMES)
    DETECTION_NMS_THRESHOLD = 0.5
    DETECTION_MIN_CONFIDENCE = 0.95
    OUTPUT = os.path.join(ROOT_DIR , 'app/static/output')
    WIDTH_TUBE = 2.5

config = InferenceConfig()
