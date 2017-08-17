docker build -t eye_classify .

docker run -it -p 8888:8888 -v $PWD/..:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify && jupyter notebook --allow-root --ip=0.0.0.0"

