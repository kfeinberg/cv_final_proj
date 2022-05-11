#object_detection

import tensorflow as tf
from imageai.Detection.Custom import DetectionModelTrainer
from tensorflow.python.client import device_lib 
print("Num GPUs Available: ", 
len(tf.config.experimental.list_physical_devices('GPU')))
#main_dir = "..\data"
data_directory = '..\data'
object_names_array = "Frisbee"
train_from_pretrained_model = "..\data\models\detection_model-ex-005--loss-0012.967.h5" #this is unique to you because it cannot be on the repo!!
trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory=data_directory)
trainer.setTrainConfig(object_names_array=[object_names_array], batch_size=4, num_experiments=60, train_from_pretrained_model=train_from_pretrained_model)
trainer.trainModel()
