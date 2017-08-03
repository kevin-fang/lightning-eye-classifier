# Eye Color Classification with Machine Learning
### Kevin Fang, Curoverse, 2017

Repository available here: https://github.com/kevin-fang/lightning-eye-classifier. 

## Project

We used support vector machines to classify genomes by eye color using genomes from the Personal Genome Project processed through the Arvados Lightning Project.

## To run the program:

Note: before running, the dependencies must be downloaded.

This project is reliant on the following Python libraries: scikit-learn, pandas, matplotlib, numpy, scipy. In addition, the tile searches cannot be run on non-UNIX machines as it requires the system `grep` and `cat` commands.

To download the numpy and assembly files needed for the project, set your Arvados API tokens and run `./download_dependencies.sh` - this downloads the tiled data, names, information, and assembly files.

To run the classifier and get the base pairs responsible for left eye color, run the Arvados workflow in `arvados_impl/` or run it through the interactive python session:  
1. First, open the iPython session using `jupyter notebook`  
2. Open `leftEyeClassifier.ipynb`, `generateAndSaveCoefs.ipynb`, and `TileSearch.ipynb`.  
3. Run `leftEyeClassifier.ipynb` first. This will generate the classifier and store it in a file called `svc.pkl`.  
4. Then run `generateAndSaveCoefs.ipynb`. This will open the `svc.pkl` classifier and save the coefficients in a file called `coefs.pkl`.  
5. Finally, run `TileSearch.ipynb`. This will open `coefs.pkl` and search for each tile.  

## Details
The classifier is able to predict the blue eye color to approximately 95% accuracy when the hazel color is excluded. Otherwise, it is able to reach 88% accuracy. 

The classifier is able to find that eye color is reliant on base pairs 28,264,893 to 28,265,118, which is consistent with the HERC2 gene, responsible for eye color (https://ghr.nlm.nih.gov/gene/HERC2#location, https://link.springer.com/article/10.1007%2Fs00439-007-0460-x)
