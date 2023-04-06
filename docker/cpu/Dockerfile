# docker build -t cresi_v3_image_cpu .
# nvidia-docker run -it --ipc=host -v /local_data:/local_data/ -p 9111:9111 --name cresi_v3 cresi_v3_image
# To use jupyter notebook, inside container run:
# jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --port=9111
# back on local machine, invoke the following in a web browser: https://localhost:9111

FROM ubuntu:18.04
MAINTAINER avanetten

# prep apt-get and cudnn
RUN apt-get update && apt-get install -y --no-install-recommends \
	    apt-utils && \
    rm -rf /var/lib/apt/lists/*

# install requirements
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
	apt-utils \
	bc \
	bzip2 \
	ca-certificates \
	curl \
	git \
	libgdal-dev \
	libssl-dev \
	libffi-dev \
	libncurses-dev \
	libgl1 \
	jq \
	nfs-common \
	parallel \
	python-dev \
	python-pip \
	python-wheel \
	python-setuptools \
	unzip \
	vim \
	tmux \
	wget \
	build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]
ENV PATH /opt/conda/bin:$PATH

# install anaconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

# use conda-forge instead of default channel
RUN conda update conda && \
    conda config --add channels conda-forge

# set up conda environment and add to $PATH
RUN conda create -n cresi python=3.6\
                    && echo "source activate cresi" > ~/.bashrc
ENV PATH /opt/conda/envs/cresi/bin:$PATH

# get pytorch
# https://pytorch.org/get-started/previous-versions/
RUN mkdir -p /root/.torch/models
RUN wget https://download.pytorch.org/models/resnet34-333f7ec4.pth -P /root/.torch/models
#RUN pip install http://download.pytorch.org/whl/cpu/torch-0.4.1-cp36-cp36m-linux_x86_64.whl \
RUN pip install http://download.pytorch.org/whl/cpu/torch-0.3.0.post4-cp36-cp36m-linux_x86_64.whl \
&& pip install torchvision \
&& pip install tensorboardX \
&& pip install utm \
&& pip install numba \
&& pip install torchsummary \
&& pip install imagecodecs

RUN conda install -n cresi fiona=1.8.20

RUN pip install geopandas
			 
RUN conda install -n cresi rasterio

RUN conda install -n cresi networkx=2.2

RUN conda install -n cresi awscli

RUN pip install pyproj==3.0.1

RUN conda install -n cresi pyhamcrest

RUN conda install -n cresi cython=0.29.24

RUN conda install -n cresi h5py=2.10.0

RUN conda install -n cresi ncurses

RUN conda install -n cresi jupyter=1.0.0

RUN conda install -n cresi jupyterlab=3.0.18

RUN conda install -n cresi matplotlib

RUN conda install -n cresi statsmodels

RUN conda install -n cresi pip

RUN conda install -n cresi pillow

RUN conda install -n cresi scipy

RUN conda install -n cresi scikit-image

RUN conda install -n cresi scikit-learn

RUN conda install -n cresi shapely

RUN conda install -n cresi rtree

RUN conda install -n cresi testpath

RUN conda install -n cresi tqdm

RUN conda install -n cresi opencv

RUN pip install osmnx

# RUN conda install -n cresi jupyter_server=1.13.1

RUN conda clean -t \
&& conda clean --yes --all
	
	
ENV LD_LIBRARY_PATH /miniconda/lib:${LD_LIBRARY_PATH}
RUN apt install -y libgl1-mesa-glx
					 
# add a jupyter kernel for the conda environment in case it's wanted
RUN source activate cresi && python -m ipykernel.kernelspec

# # clone cresi
RUN mkdir /opt/cresi/
COPY network /opt/cresi/
# RUN git clone https://github.com/avanetten/cresi.git /opt/cresi/


# TensorBoard
EXPOSE 6006
# IPython
EXPOSE 9111

WORKDIR "/opt/cresi"
RUN ["/bin/bash"]
