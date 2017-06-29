# Eye Color Classification using Support Vector Machines

Note: before running, the tiled PGP data must be downloaded and named `hiq-pgp.npy`

To run the classifier and get the base pairs responsible for left eye color, run the following command:
`python run_left_classifier_and_get_tiles.py`

Otherwise, to run it through the interactive python session:
First, open the ipython session using `jupyter notebook`
Open `leftEyeClassifier.ipynb`, `generateAndSaveCoefs.ipynb`, and `TileSearch.ipynb`. 
Run `leftEyeClassifier.ipynb` first. This will generate the classifier and store it in a file called `svc.pkl`
Then run `generateAndSaveCoefs.ipynb`. This will open the `svc.pkl` classifier and save the coefficients in a file called `coefs.pkl`
Finally, run `TileSearch.ipynb`. This will open `coefs.pkl` and search for each tile.
