FROM nvidia/cuda:10.0-base

# ENVIRONMENTS
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# INSTALL MISSING PACKAGES AND CUDA
RUN apt-get update --fix-missing && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends apt-utils gnupg2 wget bzip2 curl ca-certificates libsm6 libxext6 libxrender-dev libgtk2.0-dev python3.7 python3.7-dev python3-pip build-essential && \
    apt-get clean && apt-get autoremove

# INSTALL MINICONDA
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean --all && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    apt-get purge --autoremove -y curl wget && \
    apt-get clean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# SETUP WORKDIR
ENV PYTHONPATH="$PYTHONPATH:/opt/conda/lib/python3.7/site-packages/"
WORKDIR /home/himanshu/proctor-eyegaze-api
RUN mkdir tmp

# INSTALL APPLICATION ENVIRONMENT
COPY environment.yml .
COPY . .
RUN conda install -c anaconda cmake
RUN conda env update -f environment.yml && conda clean --all
RUN python3 get_dependencies.py

# RUN python3 -m pip install --upgrade setuptools && cd headgaze_prediction/api/deepgaze/deepgaze && python setup.py install --record record.txt && cd ../../../../

EXPOSE 5602
CMD ["gunicorn", "-k", "tornado", "run_gunicorn:APP", "-w", "3", "-b", ":5602", "--timeout", "600"]
# CMD ["python3","run.py"]
# gunicorn -k tornado --bind 0.0.0.0:5151 run:APP
