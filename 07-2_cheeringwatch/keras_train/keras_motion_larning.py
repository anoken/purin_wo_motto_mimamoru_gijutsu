## Copyright (c) 2019 aNoken
## https://twitter.com/anoken2017


from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout,Conv2D,MaxPooling2D,Flatten,ZeroPadding2D
from keras.utils.np_utils import to_categorical
from keras.optimizers import Adagrad
from keras.optimizers import Adam
import numpy as np
from PIL import Image
import os
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import itertools
import seaborn as sns

image_list = []
label_list = []

LABELS = []
label = 0

filenames = os.listdir("train")
for dir in sorted(filenames):
    dir1 = "./train/" + dir
    for file in os.listdir(dir1):
        if file != ".DS_Store":
            label_list.append(label)
            filepath = dir1 + "/" + file
            print(filepath)
            image = Image.open(filepath)
            data = np.asarray(image)
            image_list.append(data)
    label = label + 1
    LABELS.append(dir)

image_list = np.array(image_list)
image_list = image_list.astype('float32')
image_list = image_list / 255.0
Y = to_categorical(label_list)

print(Y)
print(image_list)

X_train, X_test, y_train, y_test = train_test_split(image_list, Y, test_size=0.20)


#CNN Model

model = Sequential()
input_shape=(8, 8, 3)
model.add(ZeroPadding2D(padding=((1, 1), (1, 1)), input_shape=input_shape))
model.add(Conv2D(32, (3, 3),input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding=("same")))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(label,activation='softmax'))
opt = Adam(lr=0.001)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

history=model.fit(X_train, y_train, nb_epoch=50)


def plot_graph(history):
	epochs = range(len(history.history['acc']))
	plt.plot(epochs,history.history['acc'], marker='.', label='acc')
	plt.autoscale()
	plt.title('model accuracy&loss')
	plt.grid()
	plt.xlabel('epoch')
	plt.ylabel('accuracy')
	plt.legend(loc='best')
	plt.plot(epochs,history.history['loss'], marker='.', label='loss')
	plt.autoscale()
	plt.grid()
	plt.xlabel('epoch')
	plt.ylabel('loss')
	plt.legend(loc='best')
	plt.savefig('./loss_graph.png')
	plt.show()
	
plot_graph(history)


# evaluate
score = model.evaluate(X_test, y_test, verbose=1)
print('loss=', score[0])
print('accuracy=', score[1])

#confusion_matrix
pred_y = model.predict(X_test.astype(np.float32))
pred_y_classes = np.argmax(pred_y, axis = 1) 
tue_y= np.argmax(y_test, axis = 1) 
confusion_mtx = confusion_matrix(tue_y, pred_y_classes) 
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_mtx, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d");
plt.title("Confusion matrix")
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.savefig('./confusion_matrix.png')
#plt.show();

model.save('my_model.h5')

converter = tf.lite.TFLiteConverter.from_keras_model_file('my_model.h5')
tflite_model = converter.convert()
open('my_mbnet.tflite', "wb").write(tflite_model)

import subprocess
subprocess.run(['./ncc/ncc','my_model.tflite','my_model.kmodel','-i','tflite','-o',
'k210model','--dataset','images'])


