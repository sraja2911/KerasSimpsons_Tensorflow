from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os
import sys
import tarfile
import numpy as np
import re

data_root = os.path.join('..', 'data', 'extract', 'simpsons-keras', 'kaggle_simpson_testset')

img_width, img_height = 64, 64
train_data_dir = os.path.join('..', 'data', 'extract', 'simpsons_dataset')

pre_validation_data_dir = os.path.join('..', 'data', 'extract', 'kaggle_simpson_testset')
for path in os.listdir(pre_validation_data_dir):
    if os.path.isfile(path):
        pass

validation_data_dir = os.path.join('..', 'data', 'extract', 'kaggle_simpson_testset')

nb_train_samples = 30000
nb_validation_samples = 990
epochs = 50
batch_size = 32

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (5,5), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(128, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(20))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rescale=1. / 255.0,
    shear_range=0.2,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    fill_mode='nearest',
    horizontal_flip=True
)

valid_datagen = ImageDataGenerator(rescale=1. / 255.0)

simpsons_train_data_dir = os.path.join('..', 'data', 'extract', 'simpsons_dataset')

directoryList = os.listdir(simpsons_train_data_dir)

# directoryList.remove('.')
# directoryList.remove('..')

random_char = np.random.randint(len(directoryList))

random_pics_directory = os.path.join('..', 'data', 'extract', 'simpsons_dataset', directoryList[random_char])
random_pics_list = os.listdir(random_pics_directory)
# random_pics_list.remove('.')
# random_pics_list.remove('..')

random_pic = np.random.randint(len(random_pics_list))
img_path = os.path.join(random_pics_directory, random_pics_list[random_pic])

img = load_img(img_path)
x = img_to_array(img)
x = x.reshape((1,) + x.shape)

i = 0
for batch in train_datagen.flow(x, batch_size=1, save_to_dir=os.path.join('..', 'data', 'tmp', 'simpsons'), save_format='jpeg'):
    i += 1
    if i > 10:
        break

train_generator = train_datagen.flow_from_directory(train_data_dir, target_size=(img_width, img_height), batch_size=batch_size, class_mode='categorical')

validation_generator = valid_datagen.flow_from_directory(validation_data_dir, target_size=(img_width, img_height), batch_size=batch_size, class_mode='categorical')

