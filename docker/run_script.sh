docker build -t ml-notebook .

docker run -it -p 8888:8888 -v $PWD/..:/notebooks ml-notebook /bin/bash -c "cd /notebooks && jupyter notebook"

