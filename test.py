import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
# from tensorflow.keras.datasets import mnist
fashion_mnist = tf.keras.datasets.fashion_mnist
# print(tf.__version__)
physicalDevices = tf.config.list_physical_devices('GPU')
print(physicalDevices)
tf.config.experimental.set_memory_growth(physicalDevices[0],True)


# x = tf.random.normal((2,3))
# y = tf.random.normal((3,4))
# z = tf.matmul(x,y)
# print(z)

(xTrain,yTrain),(xTest,yTest)=fashion_mnist.load_data()
xTrain = xTrain.reshape(60000,28,28,1)
xTest = xTest.reshape(10000,28,28,1)
xTrain = xTrain/255.0
xTest = xTest/255.0

# print(xTrain.shape)
# Sequential API, one input to one output

# model = keras.models.load_model('./savedModel/model.h5')
def createModel():
    model = keras.Sequential(
        [
            # layers.Conv2D(64, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            # layers.MaxPooling2D(2,2),
            # layers.Conv2D(64, (3, 3), activation='relu'),
            # layers.MaxPooling2D(2,2),
            # layers.Conv2D(64, (3, 3), activation='relu'),
            # layers.MaxPooling2D(2,2),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(10)
        ]
    )
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['sparse_categorical_accuracy']
    )
    return model

# model = createModel()
# model.fit(xTrain, yTrain, epochs=5)
# model.evaluate(xTest,yTest,verbose = 2)
# model.save('./savedModel')


newModel = tf.keras.models.load_model('./savedModel')
# Check its architecture
newModel.summary()
newModel.evaluate(xTest,yTest,verbose = 2)




# with tf.device('/gpu:0'):
#     model.fit(xTrain, yTrain, epochs=5)
#     model.evaluate(xTest,yTest,verbose = 2)
#     model.save_weights('./savedModel/')
#     model.save('./savedModel/model.h5')
# with tf.device('/cpu:0'):
#     model.fit(xTrain, yTrain, epochs=5)
#     model.evaluate(xTest,yTest,verbose = 2)