# Genomic Eye Color Classification with Machine Learning
### Kevin Fang, Curoverse 2017
[![DOI-project](https://www.zenodo.org/badge/DOI/10.5281/zenodo.843563.svg)](https://doi.org/10.5281/zenodo.843563) [![DOI-poster](https://zenodo.org/badge/DOI/10.5281/zenodo.843566.svg)](https://doi.org/10.5281/zenodo.843566)


Using machine learning and the Arvados Lightning project, we were able to predict eye color to 95% accuracy.

This project is reliant on the following Python libraries: `scikit-learn, pandas, matplotlib, numpy, scipy.` In addition, the tile searches cannot be run on non-UNIX machines as it requires the system `grep` and `cat` commands.

To download the NumPy arrays and assembly files needed for the project, [set the Arvados API tokens](https://doc.arvados.org/user/reference/api-tokens.html) and run `./download_dependencies.sh` - this downloads the tiled data, names, information, and assembly files into the appropriate folders.

### Running the classifier

First, clone the GitHub repository with `git clone --recursive https://github.com/kevin-fang/lightning-eye-classifier`. The `--recursive` is important as the tile-searching script is in a submodule.

There are three ways to run the classifier. A Dockerfile has been provided in `docker/` as well as instructions for running through Docker. 

#### Run the Python scripts by themselves:
1. Navigate to `src/`.
2. Generate the classifier with `python generateLeftClassifier.py`
3. Save the coefficients with `python saveCoefs.py`
4. Search for each tile in `python tileSearch.py`

#### Run the Arvados workflow in `arvados_impl/`

#### Run the interactive Python notebooks:  
1. First, navigate to `notebooks/`
2. Open the IPython session using `jupyter notebook`  
3. Open `leftEyeClassifier.ipynb`, `saveCoefs.ipynb`, and `tileSearch.ipynb`.  
4. Run `leftEyeClassifier.ipynb` first, and set whether to exclude or include hazel. This will generate the classifier and save it in  `svc.pkl`.  
5. Then run `saveCoefs.ipynb`. This will open the `svc.pkl` classifier and will serialize the learned coefficients in `coefs.pkl`.  
6. Finally, run `tileSearch.ipynb`. This will open `coefs.pkl` and search for each tile.  

## Details
The classifier is able to predict the blue eye color to approximately 95% accuracy when the hazel color is excluded. Otherwise, it is able to reach 88% accuracy. 

The classifier is able to find that eye color is reliant on base pairs 28,264,893 to 28,265,118, which is consistent with the HERC2 gene, responsible for eye color (https://ghr.nlm.nih.gov/gene/HERC2#location, https://link.springer.com/article/10.1007%2Fs00439-007-0460-x)
