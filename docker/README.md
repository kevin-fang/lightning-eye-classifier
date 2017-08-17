## Running through Docker

To build the docker image, run `docker build -t eye_classify .`. Before running any analysis, the dependencies must be downloaded still, so go up one directory and run `./download_dependencies.sh`

Either use the shell scripts provided (`./run_main_script.sh` and `./run_notebook.sh` to run the Python scripts and run the notebooks, respectively) or follow the instructions below:

The base command to start the interactive docker container ***from this directory*** is: `docker run -it -p 8888:8888 -v $PWD/..:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify && /bin/bash"`

For a single command that will run all the analysis, run `docker run -it -v $PWD/..:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify/src && python generateLeftClassifier.py && python saveCoefs.py && python tileSearch.py"`

**If you are in the main directory**, remove the `/..` after `$PWD`.

Once this is you are in the docker container, you can follow the instructions in the main readme for the Python scripts.

#### Run Jupyter Notebooks in Docker:

`./run_script.sh` will build a docker image with all the dependencies and run it, opening a jupyter notebook (this will take a while, depending on your internet connection and computer speed).

Run `docker run -it -p 8888:8888 -v $PWD/..:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify && jupyter notebook --allow-root --ip=0.0.0.0"` 

In the command prompt, there should be an IP address with a token that looks something like:
```
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://0.0.0.0:8888/?token=[...]
```

Open that link in your browser and then you can follow the instructions for running the notebooks in the main readme.
