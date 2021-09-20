

from mrcnn.config import Config
import os



class InferenceConfig(Config):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    NAME = "foamtastic"
    ROOT_DIR = os.path.abspath(".")
    COCO_MODEL_PATH = os.path.join(ROOT_DIR , 'app/utils/maskrcnn')
    MODEL_DIR = os.path.join( COCO_MODEL_PATH, "model_foamtastic.h5")
    CLASS_NAMES = ['bg','tube', 'cork', 'foam']
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 3
    DETECTION_NMS_THRESHOLD = 0.5
    DETECTION_MIN_CONFIDENCE = 0.95
    OUTPUT = os.path.join(ROOT_DIR , 'app/static/output')
    WIDTH_TUBE = 2.5

config = InferenceConfig()
