from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from shutil import copyfile
import os
import sys
import tarfile
import numpy as np
import re

data_root = os.path.join('..', 'data', 'extract', 'simpsons-keras', 'kaggle_simpson_testset')

img_width, img_height = 64, 64

tmp_dir = os.path.join('..', 'data', 'tmp')

fileCharacterClass = re.compile('[a-zA-Z_]+(?=[0-9]+)')

tmp_test_set_path = os.path.join(tmp_dir, 'test_set')
if not os.path.exists(tmp_test_set_path):
    os.mkdir(tmp_test_set_path)

valid_categories = []

pre_validation_data_dir = os.path.join('..', 'data', 'extract', 'kaggle_simpson_testset')
for path in os.listdir(pre_validation_data_dir):
    fullPath = os.path.join(pre_validation_data_dir, path)
    if os.path.isfile(fullPath):
        pathSplit = path.split('.')
        fileExtension = pathSplit[len(pathSplit)-1]
        if fileExtension == 'jpeg' or fileExtension == 'jpg':
            matches = fileCharacterClass.findall(path)
            newFolderPath = os.path.join(tmp_dir, 'test_set', matches[0][:len(matches[0])-1])
            valid_categories.append(matches[0][:len(matches[0])-1])
            if not os.path.exists(newFolderPath):
                os.mkdir(newFolderPath)
            newPath = os.path.join(tmp_dir, 'test_set', matches[0][:len(matches[0])-1], path)
            copyfile(fullPath, newPath)

validation_data_dir = os.path.join('..', 'data', 'extract', 'kaggle_simpson_testset')

tmp_train_set_path = os.path.join(tmp_dir, 'train_set')
if not os.path.exists(tmp_train_set_path):
    os.mkdir(tmp_train_set_path)

pre_train_data_dir = os.path.join('..', 'data', 'extract', 'simpsons_dataset')
for path in os.listdir(pre_train_data_dir):
    fullPath = os.path.join(pre_train_data_dir, path)
    if os.path.isdir(fullPath) and path in valid_categories:
        pictures_in_category = os.listdir(fullPath)
        if len(pictures_in_category) > 0:
            category_directory = os.path.join(tmp_train_set_path, path)
            if not os.path.exists(category_directory):
                os.mkdir(category_directory)
                for picturePath in pictures_in_category:
                    oldPath = os.path.join(fullPath, picturePath)
                    newPath = os.path.join(category_directory, picturePath)
                    copyfile(oldPath, newPath)


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

train_generator = train_datagen.flow_from_directory(tmp_train_set_path, target_size=(img_width, img_height), batch_size=batch_size, class_mode='categorical')

validation_generator = valid_datagen.flow_from_directory(tmp_test_set_path, target_size=(img_width, img_height), batch_size=batch_size, class_mode='categorical')

model.fit_generator(train_generator, epochs=epochs, validation_data=validation_generator)