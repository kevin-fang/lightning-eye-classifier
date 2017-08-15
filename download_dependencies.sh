echo "Downloading..."
arv-get bfba01c5b9b4053f596a2dc36d072cd6+46480/hiq-pgp .
arv-get bfba01c5b9b4053f596a2dc36d072cd6+46480/names .
cd tile-searcher && ./setup_arv.sh
echo "Finished downloading dependencies."
