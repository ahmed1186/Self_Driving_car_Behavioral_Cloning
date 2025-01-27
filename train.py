# -*- coding: utf-8 -*-


#!pip install keras==2.0.9

#!pip install keras==2.2.4

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Lambda
from keras.layers import Cropping2D

keras.__version__

img = plt.imread('./data/IMG/center_2016_12_01_13_30_48_287.jpg')
plt.imshow(img)
plt.show()

import csv
from PIL import Image
car_images=[]
steering_angles=[]

def next_batch(batch_size,shuffle=True):
  arr = np.arrange(0,49158)
  
  if shuffle==True:
    random.shuffle(arr)
  
  start_index=0

  while True:
    
    with open('./data/driving_log.csv') as csvfile:
      reader = csv.reader(csvfile)
      
    
      images=[]
      steer=[]
      reader_batch = reader[start_index:start_index+batch_size//3]

      for line in reader_batch:
        steering_center = float(line[3])
        correction=0.2
        steering_left = steering_center + correction
        steering_right = steering_center - correction

        img_path = './data/IMG/'
        line_0 = line[0].split('\\')[-1]
        line_1 = line[1].split('\\')[-1]
        line_2 = line[2].split('\\')[-1]
        img_center = np.asarray(Image.open(img_path + line_0))
        img_left = np.asarray(Image.open(img_path + line_1))
        img_right = np.asarray(Image.open(img_path + line_2))

        images.append(img_center)
        images.append(img_left)
        images.append(img_right)

        steer.append(steering_center)
        steer.append(steering_left)
        steer.append(steering_right)
        del img_center,img_left,img_right,line_0,line_1,line_2,steering_center,steering_left,steering_right

      

    
    yield np.array(images),np.array(steer)
    del images,steer

    start_index+=batch_size
    
    if (start_index>49158):
      start_index=0
      if shuffle==True:
        random.shuffle(arr)

# train_s = int(0.7*31278)
# eval_s = int(np.ceil(0.2*31278))
# test_s = int(np.ceil(0.1*31278))

# print(train_s)
# print(eval_s)
# print(test_s)

# X_train = np.array(car_images[:train_s])
# Y1_train = np.array(steering_angles[:train_s])

# X_eval = np.array(car_images[train_s:train_s+eval_s])
# Y1_eval = np.array(steering_angles[train_s:train_s+eval_s])


# X_test = np.array(car_images[train_s+eval_s:])
# Y1_test = np.array(steering_angles[train_s+eval_s:])

# print(X_train.shape)
# print(X_eval.shape)
# print(X_test.shape)

#del car_images,steering_angles,throttle,brake,speed
#del car_images,steering_angles  Didnt clear much

# import random
# import csv
# from PIL import Image

# def next_batch(batch_size,shuffle=True):
#   car_images=[]
#   steering_angles=[]
# # throttle=[]
# # brake=[]
# # speed=[]
#   while True:
#     with open('/content/One/driving_log.csv') as csvfile:
#     reader = csv.reader(csvfile)
#     for line in reader:
#       #print(line)
#       steering_center = float(line[3])
#       correction=0.2
#       steering_left = steering_center + correction
#       steering_right = steering_center - correction

#       img_path = '/content/One/IMG/'
#       line_0 = line[0].split('\\')[-1]
#       line_1 = line[1].split('\\')[-1]
#       line_2 = line[2].split('\\')[-1]
#       img_center = np.asarray(Image.open(img_path + line_0))
#       img_left = np.asarray(Image.open(img_path + line_1))
#       img_right = np.asarray(Image.open(img_path + line_2))

#       car_images[count]=img_center
#       steering_angles[count]=steering_center

#     count+=1
#     car_images[count]=img_left
#     steering_angles[count]=steering_left

#     count+=1
#     car_images[count]=img_right  
#     steering_angles[count]=steering_right

#     count+=1
#   start_index = 0
#   arr = np.arange(0,len(X_dat))
#   if shuffle==True:
#     random.shuffle(arr)
  
#   while True:
#     images = X_dat[arr[start_index:start_index+batch_size],:,:,:]
#     y_1 = y1[arr[start_index:start_index+batch_size]]
    
#     # print(images.shape)
#     # print(y_1.shape)
#     # print(y_2.shape)
#     # print(y_3.shape)
#     # print(y_4.shape)
#     #yield (images,{'output1':y_1, 'output2':y_2, 'output3':y_3,'output4':y_4})
    
#     yield images,y_1
#     del images,y_1

#     start_index+=batch_size

#     if(start_index>len(X_dat)):
#       start_index = 0
#       if shuffle==True:
#         random.shuffle(arr)

# For tensorflow 1 and keras 2.2
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D
# from tensorflow.keras.layers import MaxPooling2D
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Flatten
# from tensorflow.keras.layers import Lambda
# from tensorflow.keras.layers import Cropping2D
# from tensorflow.keras.layers import Dropout

#import tensorflow as tf

#import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.compat.v1.disable_eager_execution()

#tf.__version__

#!pip install tensorflow==1.3.0
#!pip install tensorflow-gpu==1.3.0

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(car_images,steering_angles,test_size=0.33,random_state=42)

img_size = X_train[0].shape
print(img_size)

del(car_images[:])
del(steering_angles[:])

from keras.layers import Dropout  #Remove for keras version 2.4
model  = Sequential()

model.add(Lambda(lambda x: x/255.0 - 0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((70,25),(0,0))))
model.add(Conv2D(24,(5,5),strides=(2,2),activation='relu'))
model.add(Dropout(0.5))
model.add(Conv2D(36,(5,5),strides=(2,2),activation='relu'))
model.add(Dropout(0.5))
model.add(Conv2D(48,(5,5),strides=(2,2),activation='relu'))
model.add(Dropout(0.5))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(Dropout(0.5))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.summary()

from keras.utils import plot_model
plot_model(model, to_file='model.png')

from keras.optimizers import SGD
from keras.losses import MSE

# from tensorflow.keras.optimizers import SGD
# from tensorflow.keras.losses import MSE

#Previously  optmiizer adam worked for better reudcing train loss but val loss was at 0.35 didnt decrease
opt = SGD(lr=0.001, momentum=0.9)

model.compile(optimizer='adam', loss='mse')

# batch_size = 64
# train_gen = next_batch(X_train,Y1_train,batch_size,shuffle=True)
# train_size = X_train.shape[0]
    

# valid_gen = next_batch(X_eval,Y1_eval,batch_size,shuffle=False)
# valid_size = X_eval.shape[0]



#from keras.models import load_model #Use this for keras 2.4

# from keras.callbacks import ModelCheckpoint

# filepath="weights.best.hdf5"
# checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
# callbacks_list = [checkpoint]

# history_object = model.fit_generator(
#     train_gen,
#     epochs=200,
#     steps_per_epoch = train_size//batch_size,
#     validation_data = valid_gen,
#     validation_steps = valid_size//batch_size,verbose=1
# )

# print(history_object.history.keys())
# plt.plot(history_object.history['loss'])
# plt.plot(history_object.history['val_loss'])
# plt.title('model mean squared error loss')
# plt.ylabel('mean squared error loss')
# plt.xlabel('epoch')
# plt.legend(['training set', 'validation set'], loc='upper right')
# plt.show()

X_train.shape

del Y_train

X_train = np.asarray(X_train)
#X_test = np.asarray(X_test)
Y_train = np.asarray(Y_train)
#Y_test = np.asarray(Y_test)

train_size = len(X_train)

from keras.callbacks import ModelCheckpoint

filepath="weights.best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

history_object = model.fit(
    X_train,Y_train,
    epochs=350,verbose=1,shuffle=True,steps_per_epoch = train_size//64,
    validation_split=0.2,batch_size=64,validation_steps=int(train_size*0.2/64)
)

print(history_object.history.keys())
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.show()

model.save('final_model_new.h5')

#from keras.models import load_model #Use this for keras 2.4
from tensorflow.keras.models import load_model
fin_mod = load_model('final_model_new.h5')
fin_mod.summary()

del X_train,Y_train

import csv
from PIL import Image
car_images=[]
steering_angles=[]
# throttle=[]
# brake=[]
# speed=[]
count=0
with open('/data/driving_log.csv') as csvfile:
  reader = csv.reader(csvfile)
  for line in reader:
    #print(line)
    steering_center = float(line[3])
    correction=0.2
    steering_left = steering_center + correction
    steering_right = steering_center - correction

    img_path = '/data/IMG/'
    line_0 = line[0].split('\\')[-1]
    line_1 = line[1].split('\\')[-1]
    line_2 = line[2].split('\\')[-1]
    img_center = np.asarray(Image.open(img_path + line_0))
    img_left = np.asarray(Image.open(img_path + line_1))
    img_right = np.asarray(Image.open(img_path + line_2))

    car_images.append(img_center)
    steering_angles.append(steering_center)

    
    car_images.append(img_left)
    steering_angles.append(steering_left)

    
    car_images.append(img_right)
    steering_angles.append(steering_right)

    

    del img_center,img_left,img_right,line_0,line_1,line_2,steering_center,steering_left,steering_right
    
    


print(len(car_images))
print(len(steering_angles))


# print(len(throttle))
# print(len(brake))
# print(len(speed))

from sklearn.model_selection import train_test_split
_,X_test,_,Y_test = train_test_split(car_images,steering_angles,test_size=0.33,random_state=42)

del(car_images[:])
del(steering_angles[:])



#X_train = np.asarray(X_train)
X_test = np.asarray(X_test)
#Y_train = np.asarray(Y_train)
Y_test = np.asarray(Y_test)

# testX,testY = next(next_batch(X_test,Y1_test,3128,shuffle=False))
# loss = fin_mod.evaluate(testX, testY, verbose=1)
# print('> %.3f' % (loss))

loss = fin_mod.evaluate(X_test, Y_test, verbose=1)
print('> %.3f' % (loss))

keras.__version__

model.save_weights('fin_weights.h5')

from keras.models import load_model #Use this for keras 2.4
#from tensorflow.keras.models import load_model
model.load_weights('fin_weights.h5')
model.summary()
