docker build -t eye_classify .

docker run -it -p 8888:8888 -v $PWD/..:/notebooks eye_classify /bin/bash -c "cd /notebooks && jupyter notebook --allow-root --ip=0.0.0.0"

