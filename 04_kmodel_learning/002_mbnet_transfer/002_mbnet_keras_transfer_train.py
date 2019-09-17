## Copyright (c) 2019 aNoken
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu
## This code based on "Train, Convert, Run MobileNet on Sipeed MaixPy and MaixDuino"
## http://blog.sipeed.com/p/680.html


import keras
import numpy as np
from keras import backend as K, Sequential
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras.applications.mobilenet import preprocess_input
import tensorflow as tf
from mobilenet_sipeed.mobilenet import MobileNet

NUM_CLASSES = 4
NAMES = ["001_class", "002_class", "003_class", "Unknown"]
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
TRAINING_DIR = 'dataset/train'
VALIDATION_DIR = 'dataset/vaild'

# 画像データの読み込み
imageGen=ImageDataGenerator(preprocessing_function=preprocess_input)

train_generator=imageGen.flow_from_directory(TRAINING_DIR,
	target_size=(IMAGE_WIDTH,IMAGE_HEIGHT),color_mode='rgb',
	batch_size=5,class_mode='categorical', shuffle=True)

validation_generator=imageGen.flow_from_directory(VALIDATION_DIR,
	target_size=(IMAGE_WIDTH,IMAGE_HEIGHT),color_mode='rgb',
	batch_size=5,class_mode='categorical')

# MobileNet モデルの読み込み
base_model=MobileNet(input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, 3), alpha = 0.75,depth_multiplier = 1,
 dropout = 0.001,include_top = False, weights = "imagenet", classes = 1000, backend=keras.backend, 
 layers=keras.layers,models=keras.models,utils=keras.utils)

# 出力層の追加
x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(100,activation='relu')(x)#
x=Dropout(0.5)(x)
x=Dense(50, activation='relu')(x)
preds=Dense(NUM_CLASSES, activation='softmax')(x)

mbnetModel=Model(inputs=base_model.input,outputs=preds)

for i,layer in enumerate(mbnetModel.layers):
    print(i,layer.name)

for layer in base_model.layers:
    layer.trainable = False

# モデル構成の表示
mbnetModel.summary()

# アルゴリズムを設定
mbnetModel.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])

step_size_train = (train_generator.n//train_generator.batch_size)
validation_steps = (train_generator.n//train_generator.batch_size)

# 学習開始
history=mbnetModel.fit_generator(generator=train_generator, 
	steps_per_epoch=step_size_train, epochs=50, 
	validation_data = validation_generator,validation_steps = validation_steps, verbose = 1)



from matplotlib import pyplot as plt

def plot_graph(history):
	epochs = range(len(history.history['acc']))

	plt.plot(epochs,history.history['acc'], marker='.', label='acc')
	plt.plot(epochs,history.history['val_acc'], marker='.', label='val_acc')
	plt.autoscale()
	plt.title('model accuracy')
	plt.grid()
	plt.xlabel('epoch')
	plt.ylabel('accuracy')
	plt.legend(loc='best')
	plt.savefig('./acc_graph.png')
	plt.show()
	plt.clf()
	plt.plot(epochs,history.history['loss'], marker='.', label='loss')
	plt.plot(epochs,history.history['val_loss'], marker='.', label='val_loss')
	plt.autoscale()
	plt.title('model loss')
	plt.grid()
	plt.xlabel('epoch')
	plt.ylabel('loss')
	plt.legend(loc='best')
	plt.savefig('./loss_graph.png')
	plt.show()

plot_graph(history)



#Keras モデル形式で保存
mbnetModel.save('my_mbnet.h5')

#Keras->TensorFlowLite 形式に変換
converter = tf.lite.TFLiteConverter.from_keras_model_file('my_mbnet.h5')
tflite_model = converter.convert()
open('my_mbnet.tflite', "wb").write(tflite_model)

#TensorFlowLite->kmodel 形式に変換
import subprocess
subprocess.run(['./ncc/ncc','my_mbnet.tflite','my_mbnet.kmodel','-i','tflite','-o',
'k210model','--dataset','images'])

