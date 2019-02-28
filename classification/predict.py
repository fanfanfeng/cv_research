# create by fanfan on 2019/1/4 0004
import tensorflow as tf
from tensorflow.python.platform import gfile
import os
import numpy as np
from PIL import Image
model_dir = 'tmp'
architecture = 'mobilenet_v1_1.0_224'

model_info ={}
model_info['model_file_name'] = 'output_graph.pb'
model_info['model_label_file_name'] = os.path.join(model_dir,"output_labels.txt")


model_info['final_result'] = 'final_result:0'
model_info['image_input'] = 'DecodeJPGInput:0'
if architecture == 'inception_v3':
    model_info['BottleneckInputPlaceholder'] = 'input/BottleneckInputPlaceholder:0'
    model_info['resized_input_tensor_name'] = 'Mul:0'
    model_info['bottleneck_tensor_name'] = 'pool_3/_reshape:0'
    model_info['image_decode_input'] = 'Mul_1:0'
else:
    model_info['BottleneckInputPlaceholder'] = 'input_1/BottleneckInputPlaceholder:0'
    model_info['image_decode_input'] = 'Mul:0'
    model_info['resized_input_tensor_name'] = 'input:0'
    model_info['bottleneck_tensor_name'] = 'MobilenetV1/Predictions/Reshape:0'

def restore_retrain_graph(model_info):
    with tf.Graph().as_default() as graph:
        model_path = os.path.join(model_dir, model_info['model_file_name'])
        with gfile.FastGFile(model_path,'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            resized_input_tensor,final_tesor = tf.import_graph_def(graph_def,name="",
                                                    return_elements=[
                                                                     model_info['resized_input_tensor_name'],
                                                                     model_info['final_result']])

    return graph, resized_input_tensor,final_tesor




def conver_imgage_to_vec(imageUrl):
    img = Image.open(imageUrl)
    width_origin, height_origin = img.size

    reheigh = 224
    # 缩小图片比例
    a = (int(width_origin / int(height_origin / reheigh)), reheigh)
    new_img = img.resize(a, Image.ANTIALIAS)
    new_img = new_img.resize((224, 224))
    img_ver = np.array(new_img).reshape((1,224,224,3))
    img_ver = (img_ver - 128.0) / 128.0
    return img_ver

def predict(imageUrl):
    predict_graph, resized_input_tensor,final_tesor= restore_retrain_graph(model_info)
    sess = tf.Session(graph = predict_graph)
    #with predict_graph.as_default():
    image_vec = conver_imgage_to_vec(imageUrl)


    predictions = sess.run(
        final_tesor,
        feed_dict={
            resized_input_tensor: image_vec,
        })
    return np.argmax(predictions,axis=1)


def conver_predict_to_label(predict_index):
    with gfile.FastGFile(model_info['model_label_file_name'], 'rb') as f:
        labels = f.read().decode("utf-8").strip()
        label_list = labels.split("\n")
    return label_list[predict_index]


def print_shape(tensor):
    print(tf.shape(tensor))



if __name__ == '__main__':
    imageUrl = r'E:\cv_data\treatImg\2.jpg'
    predictions = predict(imageUrl)
    print(conver_predict_to_label(predictions[0]))

