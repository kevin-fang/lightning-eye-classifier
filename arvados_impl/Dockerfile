FROM arvados/jobs
USER root

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install wget -y && \
    apt-get install dtrx -y && \
    apt-get install gcc -y && \
    apt-get install libbz2-dev -y && \
    apt-get install liblzma-dev -y && \
    apt-get install make -y && \
    wget --output-document=htslib-1.5.tar.bz2 https://github.com/samtools/htslib/releases/download/1.5/htslib-1.5.tar.bz2 && \
    dtrx htslib-1.5.tar.bz2 && \
    cd htslib-1.5 && \
    ./configure && \
    make && \
    make install

RUN apt-get install python -y && \
    apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran -y && \
    apt-get install g++ -y && \
    pip install --upgrade pip && \
    pip install numpy && \
    pip install scipy && \
    pip install pandas && \
    pip install sklearn && \
    git clone https://github.com/kevin-fang/svc-eye-classifier.git
