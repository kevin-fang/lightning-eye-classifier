## Running through Docker

To build the docker image, run `docker build -t eye_classify .`. Before running any analysis, the dependencies must be downloaded still, so go up one directory and run `./download_dependencies.sh`

The base command to start the docker container ***from this directory*** is: `docker run -it -p 8888:8888 -v $PWD/..:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify && /bin/bash"`

**If you are in the main directory**, run `docker run -it -p 8888:8888 -v $PWD:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify && /bin/bash"`

Once this is you are in the docker container, you can follow the instructions in the main readme for the Python scripts.

#### Run Jupyter Notebooks:

Run `docker run -it -p 8888:8888 -v $PWD/..:/lightning-classify eye_classify /bin/bash -c "cd /lightning-classify && jupyter notebook"`

In the command prompt, there should be an IP address with a token that looks something like:
```
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=[...]
```

Open that link in your browser and then you can follow the instructions for running the notebooks in the main readme.