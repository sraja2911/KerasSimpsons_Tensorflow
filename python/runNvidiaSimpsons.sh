nvidia-docker run \
     -it --rm -p1111:8888 \
     -v "${PWD}:/app:rw" \
     -v "/home/rsubra5/KerasSimpsons_Tensorflow/python:/data/code:rw" \
     -v "/home/rsubra5/KerasSimpsons_Tensorflow/python/results:/data/output/results:rw" \
     -v "/home/rsubra5/simpsonsdata/train:/data/train:rw" \
     -v "/home/rsubra5/simpsonsdata/test:/data/test:rw" \
     fgiuste/neuroml:V3
