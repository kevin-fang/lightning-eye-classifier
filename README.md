# Eye Color Classification using Support Vector Machines
### Kevin Fang, Curoverse, 2017
Note: before running, the tiled PGP data must be downloaded and named `hiq-pgp.npy`. In addition, the tiled datasets must be downloaded - this includes `assembly.00.hg19.fw.fwi` and `assembly.00.hg10.fw.gz`. There are instructions for downloading the assembly files in `/tiling/`

This project is reliant on the following Python libraries: scikit-learn, pandas, matplotlib, numpy, scipy. In addition, the tile searches cannot be run on non-UNIX machines as it requires the system `grep` and `cat` commands.

To setup the entire repository, setup your Arvados API tokens and run `./download_dependencies.sh` - this downloads the tiled data, names, information, and assembly files.

To run the classifier and get the base pairs responsible for left eye color, run the following command:
`python run_left_classifier_and_get_tiles.py`

Otherwise, to run it through the interactive python session:  
1. First, open the iPython session using `jupyter notebook`  
2. Open `leftEyeClassifier.ipynb`, `generateAndSaveCoefs.ipynb`, and `TileSearch.ipynb`.  
3. Run `leftEyeClassifier.ipynb` first. This will generate the classifier and store it in a file called `svc.pkl`.  
4. Then run `generateAndSaveCoefs.ipynb`. This will open the `svc.pkl` classifier and save the coefficients in a file called `coefs.pkl`.  
5. Finally, run `TileSearch.ipynb`. This will open `coefs.pkl` and search for each tile.  

## Details
The classifier is able to predict the blue eye color to approximately 85% accuracy. Using 10-fold cross validation, an accuracy of 85.6% +/- 9.46% is achieved. With leave-one-out cross validation, an accuracy of 87.2% is achieved. Below is a confusion matrix for the leave-one-out cross validation:

![confusion-matrix][https://github.com/kevin-fang/svc-eye-classifier/raw/master/Blue_Confusion.png]
