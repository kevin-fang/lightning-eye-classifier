docker build -t eye_classify .

docker run -it -v $PWD/..:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify/src && python generateLeftClassifier.py && python saveCoefs.py && python tileSearch.py"