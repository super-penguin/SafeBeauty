# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
# #==========================================================================

FROM tensorflow/tensorflow:nightly-devel

# Get the tensorflow models research directory, and move it into tensorflow
# source folder to match recommendation of installation
RUN git clone --depth 1 https://github.com/tensorflow/models.git && \
    mv models /tensorflow/models

# Install the Tensorflow Object Detection API from here
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

# Install object detection api dependencies
RUN pip install Werkzeug Flask numpy Keras gevent pillow h5py Cython contextlib2 jupyter matplotlib

# Run protoc on the object detection repo
RUN cd /tensorflow/models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH $PYTHONPATH:/tensorflow/models/research:/tensorflow/models/research/slim


# Install wget (to make life easier below) and editors (to allow people to edit
# the files inside the container)
RUN apt-get install -y wget vim emacs nano

# Copy the files into the container
COPY . /usr/src/app

# Set the working directory
WORKDIR /usr/src/app

# Install the dependencies
RUN pip install Werkzeug Flask numpy Keras gevent pillow h5py tensorflow

# Expose the port
EXPOSE 5000

# Run the app
CMD [ "python" , "penny_learn.py"]
