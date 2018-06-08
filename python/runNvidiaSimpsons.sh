docker run \
    --runtime=nvidia \
    -ti \
    -v "${PWD}:/app" \
    -v "/home/dagutman/devel/KerasSimpsons_Tensorflow/rawImageData/:/imageData" \
    tensorflow/tensorflow:latest-gpu \
    # python /app/runSimpsonsModel_NvidiaDocker.py 

  	# jupyter/tensorflow-notebook \
    # --rm \


