FROM arvados/jobs
USER root

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y wget \
	dtrx \
	gcc \
	libbz2-dev \
	liblzma-dev \
	make && \
    wget --output-document=htslib-1.5.tar.bz2 https://github.com/samtools/htslib/releases/download/1.5/htslib-1.5.tar.bz2 && \
    dtrx htslib-1.5.tar.bz2 && \
    cd htslib-1.5 && \
    ./configure && \
    make && \
    make install

RUN apt-get install -y python \
	libblas-dev \
	liblapack-dev \
	libatlas-base-dev \
	gfortran \
	g++ && \
    pip install --upgrade pip && \
    pip install numpy \
	scipy \
	pandas \
	sklearn 
