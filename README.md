# Eye Color Classification using Support Vector Machines
### Kevin Fang, Curoverse, 2017
Note: before running, the tiled PGP data must be downloaded and named `hiq-pgp.npy`. In addition, the tiled datasets must be downloaded - this includes `assembly.00.hg19.fw.fwi` and `assembly.00.hg10.fw.gz`. There are instructions for downloading the assembly files in `/tiling/`

This project is reliant on the following Python libraries: scikit-learn, pandas, matplotlib, numpy, scipy. In addition, the tile searches cannot be run on non-UNIX machines as it requires the system `grep` and `cat` commands.

To download hiq-pgp.npy, stay in this folder and run `arv-get bfba01c5b9b4053f596a2dc36d072cd6+46480/hiq-pgp .` after setting your Arvados API key.

To setup in this entire project in one command, run `arv-get bfba01c5b9b4053f596a2dc36d072cd6+46480/hiq-pgp . && cd tiling && arv-get b8835cbca4f8dfd3396f39f5ca10bb84+780/assembly.00.hg19.fw.fwi . && arv-get b8835cbca4f8dfd3396f39f5ca10bb84+780/assembly.00.hg19.fw.gz .`

To run the classifier and get the base pairs responsible for left eye color, run the following command:
`python run_left_classifier_and_get_tiles.py`

Otherwise, to run it through the interactive python session:  
1. First, open the iPython session using `jupyter notebook`  
2. Open `leftEyeClassifier.ipynb`, `generateAndSaveCoefs.ipynb`, and `TileSearch.ipynb`.  
3. Run `leftEyeClassifier.ipynb` first. This will generate the classifier and store it in a file called `svc.pkl`.  
4. Then run `generateAndSaveCoefs.ipynb`. This will open the `svc.pkl` classifier and save the coefficients in a file called `coefs.pkl`.  
5. Finally, run `TileSearch.ipynb`. This will open `coefs.pkl` and search for each tile.  
