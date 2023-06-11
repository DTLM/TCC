# -*- coding: utf-8 -*-
"""TCC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1odqpQY73kKQ4TZo8wz9gGx_m-i4_UYNq
    
comandos de instalação de pacotes:
1 - pip install matplotlib
2 - pip install tensorflow
3 - pip install scikit-learn
"""

from matplotlib import pyplot
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import sys
from matplotlib import pyplot
from  tensorflow.keras.models import Sequential
from  tensorflow.keras.layers import Conv2D
from  tensorflow.keras.layers import MaxPooling2D
from  tensorflow.keras.layers import Dense
from  tensorflow.keras.layers import Flatten
from  tensorflow.keras.optimizers import SGD
from  tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dropout
from  tensorflow.keras.metrics import Precision
from  tensorflow.keras.metrics import Recall
import cv2
from factoryFilter import prepareAmbiente

# caminhos
absPath = os.getcwd()
baseFolder = "\\Dados\\"
caminhoTesteFinal = absPath + "\\fotos para testes de predict"

# noise
caminhoNoiseTreinoGrupo = absPath + baseFolder + "noise filter\\" + "treino grupo"
caminhoNoiseTesteGrupo = absPath + baseFolder + "noise filter\\" + "teste grupo"
caminhoNoiseTreinoDoencas = absPath + baseFolder + "noise filter\\" + "treino doencas"
caminhoNoiseTesteDoencas = absPath + baseFolder + "noise filter\\" + "teste doencas"

# peper
caminhoPeperTreinoGrupo = absPath + baseFolder + "peper filter\\" + "treino grupo"
caminhoPeperTesteGrupo = absPath + baseFolder + "peper filter\\" + "teste grupo"
caminhoPeperTreinoDoencas = absPath + baseFolder + "peper filter\\" + "treino doencas"
caminhoPeperTesteDoencas = absPath + baseFolder + "peper filter\\" + "teste doencas"

# filtro duplo
caminhoDuploTreinoGrupo = absPath + baseFolder + "filtro duplo\\" + "treino grupo"
caminhoDuploTesteGrupo = absPath + baseFolder + "filtro duplo\\" + "teste grupo"
caminhoDuploTreinoDoencas = absPath + baseFolder + "filtro duplo\\" + "treino doencas"
caminhoDuploTesteDoencas = absPath + baseFolder + "filtro duplo\\" + "teste doencas"

# sem filtro
teste = './Dados/test diseases/'
treino = './Dados/train diseases/'
testeGrupo = './Dados/test grupos/'
treinoGrupo = './Dados/train grupos/'

# load and prepare the image
def load_image(filename):
 # load the image
 img = load_img(filename, target_size=(224, 224))
 # convert to array
 img = img_to_array(img)
 # reshape into a single sample with 3 channels
 img = img.reshape(1, 224, 224, 3)
 # center pixel data
 img = img.astype('float32')
 img = img - [123.68, 116.779, 103.939]
 return img

# plot diagnostic learning curves
def summarize_diagnostics(history):
	# plot loss
	pyplot.subplot(211)
	pyplot.title('Cross Entropy Loss')
	pyplot.plot(history.history['loss'], color='blue', label='train')
	pyplot.plot(history.history['val_loss'], color='orange', label='test')
	# plot accuracy
	pyplot.subplot(212)
	pyplot.title('Classification Accuracy')
	pyplot.plot(history.history['accuracy'], color='blue', label='train')
	pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
	# save plot to file
	filename = sys.argv[0].split('/')[-1]
	pyplot.savefig(filename + " peper filtro doença" + '_plot.png')
	pyplot.close()

"""Tecnicas a verificar pra pre tratamento de imagens: 
1 noise removal: https://stackoverflow.com/questions/62042172/how-to-remove-noise-in-image-opencv-python
2 - normalização
3 - Image augmentation: https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/
4 - dropout regularization: https://machinelearningmastery.com/how-to-reduce-overfitting-with-dropout-regularization-in-keras/
5 - salt and peper noise: https://www.geeksforgeeks.org/add-a-salt-and-pepper-noise-to-an-image-with-python/
"""

# define cnn model
def define_model():
 model = Sequential()
 model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(200, 200, 3)))
 model.add(MaxPooling2D((2, 2)))
 # Dropout regularization from https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/
 model.add(Dropout(0.2))
 
 model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
 model.add(MaxPooling2D((2, 2)))
 model.add(Dropout(0.2))
 
 model.add(Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
 model.add(MaxPooling2D((2, 2)))
 model.add(Dropout(0.2))
 
 model.add(Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
 model.add(MaxPooling2D((2, 2)))
 model.add(Dropout(0.2))

 model.add(Conv2D(512, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
 model.add(MaxPooling2D((2, 2)))
 model.add(Dropout(0.2))

 model.add(Conv2D(1024, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
 model.add(MaxPooling2D((2, 2)))
 model.add(Dropout(0.2))

 model.add(Conv2D(2048, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
 model.add(MaxPooling2D((2, 2)))
 model.add(Dropout(0.2))
	
 model.add(Flatten())
 model.add(Dense(2048, activation='relu', kernel_initializer='he_uniform'))
 model.add(Dropout(0.5))
 model.add(Dense(18, activation="softmax")) # camada de saida
 

 # compile model
 opt = SGD(learning_rate=0.001, momentum=0.9)
 model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy', Precision(), Recall()])
 return model

#run the training and test of ML with CNN
def run_test():
 # prepara o ambiente, pegando as imagens e aplicando os filtros. Em resumo está fazendo o pre-tratamento da imagem
# prepareAmbiente()

 # define cnn model
 model = define_model()

 # create data generator for train, normalizate the data (1.0/255.0), Image data augmentation (width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)
 #from https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/
 train_datagen = ImageDataGenerator(rescale = 1.0/255.0, width_shift_range=0.1, height_shift_range=0.1, horizontal_flip = True)
 # create data generator for tests and normalizate the data (1.0/255.0)
 datagen = ImageDataGenerator(rescale=1.0/255.0)

 # Train and Test part
 # prepare iterators
 train_it = train_datagen.flow_from_directory(caminhoPeperTreinoDoencas,
	class_mode='categorical', batch_size=64, target_size=(200, 200))
 test_it = datagen.flow_from_directory(caminhoPeperTesteDoencas,
	class_mode='categorical', batch_size=64, target_size=(200, 200))

 # fit model
 history = model.fit(train_it, steps_per_epoch=len(train_it),
	validation_data=test_it, validation_steps=len(test_it), epochs=40, verbose=1)

 # evaluate model
 _, acc, prec, rec = model.evaluate(test_it, steps=len(test_it), verbose=0)
 print('> %.3f' % (acc * 100.0))
 print('> %.3f' % (prec * 100.0))
 print('> %.3f' % (rec * 100.0))
 
 # learning curves
 summarize_diagnostics(history)

 for image in os.listdir(caminhoTesteFinal):
  caminhoImageTeste = caminhoTesteFinal + "\\" + image
  if(os.path.exists(caminhoImageTeste)):
   img = load_image(caminhoImageTeste)
#    pyplot.imshow(img)
#    pyplot.show()
   result = model.predict(img)
   print(result[0])
  else:
   print("caminho não existe.")

run_test()