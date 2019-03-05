# create by fanfan on 2019/1/24 0024
import tensorflow as tf
import sys


import os

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
def sample_convert_tflite():
    img = tf.placeholder(name="img", dtype=tf.float32, shape=(1, 64, 64, 3))
    var = tf.get_variable("weights", dtype=tf.float32, shape=(1, 64, 64, 3))
    val = img + var
    out = tf.identity(val, name="out")

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        converter = tf.contrib.lite.TFLiteConverter.from_session(sess, [img], [out])
        tflite_model = converter.convert()
        open("converted_model.tflite", "wb").write(tflite_model)

from tensorflow.contrib.lite.toco.types_pb2 import QUANTIZED_UINT8,FLOAT

def convert_pb_to_tflite():
    model_path = os.path.join(model_dir, model_info['model_file_name'])
    input_arrays = [model_info['resized_input_tensor_name'].replace(":0","")]
    output_arrays = [model_info['final_result'].replace(":0","")]
    input_shapes = [(1,224,224,3)]
    input_shapes_dict = {}
    for shape,name in zip(input_shapes,input_arrays):
        input_shapes_dict[name] = shape

    converter = tf.contrib.lite.TFLiteConverter.from_frozen_graph(
        model_path, input_arrays, output_arrays,input_shapes_dict)
    converter.inference_type = QUANTIZED_UINT8
    #converter.inference_input_type = FLOAT
    print(converter.inference_input_type) 
    converter.quantized_input_stats = {model_info['resized_input_tensor_name'].replace(":0",""): (127.5, 127.5)}
    converter.default_ranges_stats = (0, 6)

    tflite_model = converter.convert()
    open("converted_model.tflite", "wb").write(tflite_model)


def conver_smooth_to_tflite():
    '''吸烟模型'''
    model_path = r'/data/python_project/cv_research/smooth/smoking-faces-output-graph.pb'
    input_arrays = ['input']
    output_arrays = ['final_result']

    converter = tf.contrib.lite.TFLiteConverter.from_frozen_graph(
        model_path, input_arrays, output_arrays)

    tflite_model = converter.convert()
    open("smooth_model.tflite", "wb").write(tflite_model)


def error_msg():
    msg = b"\xb2\xbb\xca\xc7\xc4\xda\xb2\xbf\xbb\xf2\xcd\xe2\xb2\xbf\xc3\xfc\xc1\xee\xa3\xac\xd2\xb2\xb2\xbb\xca\xc7\xbf\xc9\xd4\xcb\xd0\xd0\xb5\xc4\xb3\xcc\xd0\xf2\r\n\xbb\xf2\xc5\xfa\xb4\xa6\xc0\xed\xce\xc4\xbc\xfe\xa1\xa3"
    print(msg.decode('gbk'))
if __name__ == '__main__':

    conver_smooth_to_tflite()
