# create by fanfan on 2019/1/24 0024
import tensorflow as tf
import argparse


import os


model_info ={}
model_info['final_result'] = 'final_result:0'
model_info['inception_v3'] = {}
model_info['mobilenet'] = {}
# inceptionv3 输入输出节点的名称
model_info['inception_v3']['resized_input_tensor_name'] = 'Mul:0'
# mobilenet 输入输出节点的名称
model_info['mobilenet']['resized_input_tensor_name'] = 'input:0'

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

def convert_pb_to_tflite_quate(model_path,input_name,output_name,output_tflite,use_quote=False):
    input_arrays = [input_name.replace(":0","")]
    output_arrays = [output_name.replace(":0","")]
    input_shapes = [(1,224,224,3)]
    input_shapes_dict = {}
    for shape,name in zip(input_shapes,input_arrays):
        input_shapes_dict[name] = shape

    converter = tf.contrib.lite.TFLiteConverter.from_frozen_graph(
        model_path, input_arrays, output_arrays,input_shapes_dict)

    if use_quote:
        converter.inference_type = QUANTIZED_UINT8
        converter.quantized_input_stats = {input_name.replace(":0",""): (127.5, 127.5)}
        converter.default_ranges_stats = (0, 6)

    tflite_model = converter.convert()
    open(output_tflite, "wb").write(tflite_model)




def conver_smooth_to_tflite():
    '''吸烟模型'''
    model_path = r'/data/python_project/cv_research/smooth/smoking-faces-output-graph.pb'
    input_arrays = ['input']
    output_arrays = ['final_result']

    converter = tf.contrib.lite.TFLiteConverter.from_frozen_graph(
        model_path, input_arrays, output_arrays)

    tflite_model = converter.convert()
    open("smooth_model.tflite", "wb").write(tflite_model)



def get_args():
    '''
    参数解析器，获取执行的参数
    :return: 
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-output_dir",type=str,default="tmp",help="处理以后的输出目录")
    parser.add_argument("-output_name", type=str, default="graph.lite", help="输出的tflite文件名")
    parser.add_argument('-use_quote',action='store_true',default=False,help='是否转化为quote的模型')
    parser.add_argument('-input_pb_dir',type=str,default="tmp",help="带转化pb模型文件目录")
    parser.add_argument('-input_pb_name', type=str, default="output_graph.pb", help="带转name化pb模型文件目录")
    parser.add_argument('-architecture',type=int,default=0,help="0 代表mobienet ,1代表inception")
    return  parser.parse_args()

if __name__ == '__main__':
    argv = get_args()

    pb_model_path = os.path.join(argv.input_pb_dir,argv.input_pb_name)
    output_lite_path = os.path.join(argv.output_dir,argv.output_name)
    use_quote = argv.use_quote
    if argv.architecture == 0:
        input_node_name = model_info['mobilenet']['resized_input_tensor_name']
    else:
        input_node_name = model_info['inception_v3']['resized_input_tensor_name']
    output_node_name = model_info['final_result']

    convert_pb_to_tflite_quate(model_path=pb_model_path,input_name=input_node_name,output_name=output_node_name,output_tflite=output_lite_path,use_quote=use_quote)
