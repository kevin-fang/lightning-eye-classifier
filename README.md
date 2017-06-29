# Eye Color Classification using Support Vector Machines
### Kevin Fang, Curoverse, 2017
Note: before running, the tiled PGP data must be downloaded and named `hiq-pgp.npy`. In addition, the tiled datasets must be downloaded - this includes `assembly.00.hg19.fw.fwi` and `assembly.00.hg10.fw.gz`.

To run the classifier and get the base pairs responsible for left eye color, run the following command:
`python run_left_classifier_and_get_tiles.py`

Otherwise, to run it through the interactive python session:  
1. First, open the ipython session using `jupyter notebook`  
2. Open `leftEyeClassifier.ipynb`, `generateAndSaveCoefs.ipynb`, and `TileSearch.ipynb`.  
3. Run `leftEyeClassifier.ipynb` first. This will generate the classifier and store it in a file called `svc.pkl`.  
4. Then run `generateAndSaveCoefs.ipynb`. This will open the `svc.pkl` classifier and save the coefficients in a file called `coefs.pkl`.  
5. Finally, run `TileSearch.ipynb`. This will open `coefs.pkl` and search for each tile.  
