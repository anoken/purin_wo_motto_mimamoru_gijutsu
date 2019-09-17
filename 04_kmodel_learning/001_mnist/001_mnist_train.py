## Copyright (c) 2019 aNoken
## https://anoken.jimdo.com/
## https://github.com/anoken/purin_wo_motto_mimamoru_gijutsu

from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras import backend as K
import tensorflow as tf
from matplotlib import pyplot as plt

#パラメータ
batch_size = 128
num_classes = 10
epochs = 10
img_rows, img_cols = 28, 28

# MNIST モデルを読み込み・整形
def prepare_mnist_data():
	(x_train, y_train), (x_test, y_test) = mnist.load_data()

	x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
	x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
	input_shape = (img_rows, img_cols, 1)
	
	x_train = x_train.astype('float32')
	x_test = x_test.astype('float32')
	x_train /= 255
	x_test /= 255
	print('x_train shape:', x_train.shape)
	print(x_train.shape[0], 'train samples')
	print(x_test.shape[0], 'test samples')
	
	y_train = keras.utils.to_categorical(y_train, num_classes)
	y_test = keras.utils.to_categorical(y_test, num_classes)
	
	return (x_train, y_train), (x_test, y_test)

(x_train, y_train), (x_test, y_test)=prepare_mnist_data()

def create_mnist_model(input_shape=(img_rows, img_cols, 1), num_classes=10):
	num_classes = 10
	kernel_size=(3, 3)
	pool_size=(2, 2)

	model = Sequential()
	
	model.add(ZeroPadding2D(padding=((1, 1), (1, 1)), input_shape=input_shape))
	model.add(Conv2D(32, kernel_size,activation='relu',input_shape=input_shape))
	model.add(MaxPooling2D(pool_size))

	model.add(ZeroPadding2D(padding=((1, 1), (1, 1))))
	model.add(Conv2D(64, kernel_size,activation='relu'))
	model.add(MaxPooling2D(pool_size))

	model.add(Dropout(0.25))
	model.add(Flatten())
	model.add(Dense(128, activation='relu')) 
	model.add(Dropout(0.5))
	model.add(Dense(num_classes, activation='softmax'))
	return model
model = create_mnist_model()

# モデル構成を表示
model.summary()

# アルゴリズムを設定
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

for layer in model.layers:
	print(layer.name)

# 学習開始
history=model.fit(x_train, y_train, batch_size=batch_size,
          epochs=epochs,verbose=1,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# 結果をグラフで表示
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
model.save("mnist.h5")

#Keras->TensorFlowLite 形式に変換
converter = tf.lite.TFLiteConverter.from_keras_model_file('mnist.h5')
tflite_model = converter.convert()
open('mnist.tflite', "wb").write(tflite_model)

#TensorFlowLite->kmodel 形式に変換
import subprocess
subprocess.run(['./ncc/ncc','mnist.tflite','mnist.kmodel','-i','tflite','-o',
'k210model','--dataset','images'])














