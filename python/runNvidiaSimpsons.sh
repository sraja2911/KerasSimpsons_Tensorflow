docker run \
    --runtime=nvidia \
    --rm \
    -ti \
    -v "${PWD}:/app" \
    -v "/home/dagutman/devel/KerasSimpsons_Tensorflow/rawImageData/:/imageData" \
  	jupyter/tensorflow-notebook \
    python /app/runSimpsonsModel_NvidiaDocker.py gpu 10000 



##    tensorflow/tensorflow:latest-gpu \
