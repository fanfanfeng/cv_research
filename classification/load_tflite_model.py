# create by fanfan on 2019/1/28 0028
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.python.platform import gfile
print(tf.__version__)
import os
model_dir = 'tmp'



model_info ={}
model_info['model_label_file_name'] = os.path.join(model_dir,"output_labels.txt")

def conver_imgage_to_vec(imageUrl,quote_model=False):
    img = Image.open(imageUrl)
    width_origin, height_origin = img.size

    reheigh = 224
    # 缩小图片比例
    a = (int(width_origin / int(height_origin / reheigh)), reheigh)
    new_img = img.resize(a, Image.ANTIALIAS)
    new_img = new_img.resize((224, 224))
    img_ver = np.array(new_img).reshape((1,224,224,3))
    if not quote_model:
        img_ver = (img_ver - 128.0) / 128.0
        img_ver = img_ver.astype(np.float32)
    return img_ver

import  sys
if 'win' in sys.platform:
    imageUrl = r'E:\cv_data\treatImg\2.jpg'
else:
    imageUrl = r'/data/cv_model/treatImg/2.jpg'
image_vec = conver_imgage_to_vec(imageUrl,quote_model=True)




# load TFLite model and allocate tensors.
interperter = tf.contrib.lite.Interpreter(model_path="converted_model.tflite")
interperter.allocate_tensors()


# Get input and output tensors.
input_details = interperter.get_input_details()
output_details = interperter.get_output_details()

print(input_details)
print(output_details)

interperter.set_tensor(input_details[0]['index'],image_vec)
interperter.invoke()
output_data = interperter.get_tensor(output_details[0]['index'])
print(output_data)


def conver_predict_to_label(predict_index):
    with gfile.FastGFile(model_info['model_label_file_name'], 'rb') as f:
        labels = f.read().decode("utf-8").strip()
        label_list = labels.split("\n")
    return label_list[predict_index]
predictions = np.argmax(output_data,axis=1)
print(conver_predict_to_label(predictions[0]))

