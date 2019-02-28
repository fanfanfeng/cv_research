# create by fanfan on 2019/1/11 0011
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Read and preprocess image data.
 Image processing occurs on a single image at a time. Image are read and
 preprocessed in parallel across multiple threads. The resulting images
 are concatenated together to form a single batch for training or evaluation.
 -- Provide processed image data for a network:
 inputs: Construct batches of evaluation examples of images.
 distorted_inputs: Construct batches of training examples of images.
 batch_inputs: Construct batches of training or evaluation examples of images.
 -- Data processing:
 parse_example_proto: Parses an Example proto containing a training example
   of an image.
 -- Image decoding:
 decode_jpeg: Decode a JPEG encoded string into a 3-D float32 Tensor.
 -- Image preprocessing:
 image_preprocessing: Decode and preprocess one image for evaluation or training
 distort_image: Distort one image for training a network.
 eval_image: Prepare one image for evaluation.
 distort_color: Distort the color in one image for training.
"""

import tensorflow as tf
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('batch_size',32,'Number of images to process in a batch.')
tf.app.flags.DEFINE_integer('image_size',299,'Provide square images of this size.')
tf.app.flags.DEFINE_integer("num_perprocess_threads",4,"Number of preprocessing threads per tower.Please make this a multiple of 4.")
tf.app.flags.DEFINE_integer("num_readers",4,'Number of parallel readers during train.')
tf.app.flags.DEFINE_integer("input_queue_memory_factor",16,
                            """Size of the queue of preprocessed images. """
                            """Default is ideal but try smaller values, e.g. """
                            """4, 2 or 1, if host memory is constrained. See """
                            """comments in code for more details."""
                            )

def inputs(datasets,batch_size = None,num_preprocess_threads=None):
    """Generate batches of ImageNet images for evaluation.
      Use this function as the inputs for evaluating a network.
      Note that some (minimal) image preprocessing occurs during evaluation
      including central cropping and resizing of the image to fit the network.
      Args:
        dataset: instance of Dataset class specifying the dataset.
        batch_size: integer, number of examples in batch
        num_preprocess_threads: integer, total number of preprocessing threads but
          None defaults to FLAGS.num_preprocess_threads.
      Returns:
        images: Images. 4D tensor of size [batch_size, FLAGS.image_size,
                                           image_size, 3].
        labels: 1-D integer Tensor of [FLAGS.batch_size].
      """
    if not batch_size:
        batch_size = FLAGS.batch_size

    # Force all input processing onto CPU in order to reserve the GPU for
    # the forward inference and back-propagation.

    with tf.device('/cpu:0'):
        pass


def batch_inputs(dataset,batch_size,train,num_preprocess_threads=None,num_readers=1):
    """Contruct batches of training or evaluation examples from the image dataset.
      Args:
        dataset: instance of Dataset class specifying the dataset.
          See dataset.py for details.
        batch_size: integer
        train: boolean
        num_preprocess_threads: integer, total number of preprocessing threads
        num_readers: integer, number of parallel readers
      Returns:
        images: 4-D float Tensor of a batch of images
        labels: 1-D integer Tensor of [batch_size].
      Raises:
        ValueError: if data is not found
      """
    with tf.name_scope('batch_processing'):
        data_files = dataset.data_files()
        if data_files is None:
            raise ValueError("No data files found for this dataset")

