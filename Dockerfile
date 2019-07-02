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

FROM python:slim-stretch

RUN apt-get update -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y --no-install-recommends \
	build-essential \
	ca-certificates \
	check \
	cmake \
	cython3 \
	git \
        libcap2-bin \
	libcurl4-openssl-dev \
	libemu-dev \
	libev-dev \
	libglib2.0-dev \
	libloudmouth1-dev \
	libnetfilter-queue-dev \
	libnl-3-dev \
	libpcap-dev \
	libssl-dev \
	libtool \
	libudns-dev \
	procps \
	python3 \
	python3-dev \
	python3-bson \
	python3-yaml \
	ttf-liberation \
    libsm6 \
    libxext6 \
    libxrender-dev

# Install object detection api dependencies
RUN pip install pandas Werkzeug Flask numpy Keras gevent pillow h5py Cython contextlib2 tensorflow jupyter matplotlib opencv-python

# Copy the files into the container
COPY . /usr/src/app

# Set the working directory
WORKDIR /usr/src/app

# Expose the port
EXPOSE 5000

# Run the app
CMD [ "python" , "penny_learn.py"]
