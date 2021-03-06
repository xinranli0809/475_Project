import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# comment these off if giving you error
# physicalDevices = tf.config.list_physical_devices('GPU')
# print(physicalDevices)
# tf.config.experimental.set_memory_growth(physicalDevices,True)

## To use more than one attributes, we will do the same number of 2 class classification over all attributes
#what characteristic are we going to train and test for? (note if set to 'all' it'll use all of them)
ATTR= ['Male','Attractive','Eyeglasses','Wearing_Hat']

# set up working directory
currentWorkingDirectory = os.getcwd()
imageDirectory = 'C:/Users/nalex/Downloads/img_align_celeba/img_align_celeba/'
attributesDirectory = 'list_attr_celeba.csv'
partitionsDirectory = 'list_eval_partition.csv'

# read the attributes and image data partition file
attributes = pd.read_csv(attributesDirectory)
partitions = pd.read_csv(partitionsDirectory)

# modify the attributes file so that the index is the name of the image
attributes.set_index('image_id', inplace=True)
# and replace all -1 to 0
attributes.replace(to_replace=-1, value=0, inplace=True)
# print(attributes.shape)

# if ATTR='all', then set ATTR equals to the name of every column in attributes
if(ATTR=='all'):
    ATTR=list(attributes.columns)


# modify the partitions file so that the index is the name of the image
# print(partitions['partition'].value_counts().sort_index())
partitions.set_index('image_id', inplace=True)


parAttr = partitions.join(attributes[ATTR], how='inner')
# print(parAttr.shape)

def load_reshape_img(fname):
    # Load image as PIL format
    img = keras.preprocessing.image.load_img(fname)
    # Convert image to np array and normalize
    x = keras.preprocessing.image.img_to_array(img)/255.
    # reshape into shape of [1, 218, 178, 3]
    x = x.reshape((1,) + x.shape)

    # These should do the exact same thing.
    # fname = imageDirectory+str(fname)
    # img = np.asarray(PIL.Image.open(fname))/255.
    # img = img.reshape((1,) + img.shape)

    return x

def generate_df(df,partition, attr, num_samples):
    '''
    partition
        0 -> train
        1 -> validation
        2 -> test
    '''
    ## This part is to balance the sample size for overly common or very uncommon attributes.
    ##  Considering adding back in the future 

    #The sample size is at most the number stated above, but at least the size of the smallest class of the dataframe. This results in some uncommon attributes (e.g. sideburns) having to train on very few samples.
    # min_class_size=min(len(df[(df['partition'] == partition) & (df[attr] == 0)]),len(df[(df['partition'] == partition) & (df[attr] == 1)]) )
    # sample_size=int(num_samples/2)
    # if(min_class_size<int(num_samples/2)):
    #     sample_size=min_class_size
    
    # df_ = df[(df['partition'] == partition) & (df[attr] == 0)].sample(sample_size)
    # df_ = pd.concat([df_,
    #                   df[(df['partition'] == partition) 
    #                               & (df[attr] == 1)].sample(sample_siz)])


    # sample desired amount of images of input partition
    df_ = df[(df['partition'] == partition)].sample(num_samples)
    # print(df_)

    x_ = np.array([load_reshape_img(imageDirectory + fname) for fname in df_.index])
    # reshape into shape of [# of samples, 218, 178, 3]
    x_ = x_.reshape(x_.shape[0], 218, 178, 3)
    # one-hot encode the y values
    y_ = keras.utils.to_categorical(df_[attr],2)

    ## This part is commented out because I don't understand why training and test data are processed in
    ## very different ways yet in the end has the same shape. Use the above method for both train and test for now 
    
    # # for Train and Validation
    # if partition != 2:
    #     # load images into shape of [number of images, 1, 218, 178, 3]
    #     x_ = np.array([load_reshape_img(imageDirectory + fname) for fname in df_.index])
    #     # reshape into the input shape for the model
    #     x_ = x_.reshape(x_.shape[0], 218, 178, 3)
    #     y_ = keras.utils.to_categorical(df_[attr],2)
    # # for Test
    # else:
    #     x_ = []
    #     y_ = []

    #     for index, target in df_.iterrows():
    #         im = cv2.imread(imageDirectory + index)
    #         im = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2RGB), (IMG_WIDTH, IMG_HEIGHT)).astype(np.float32) / 255.0
    #         im = np.expand_dims(im, axis =0)
    #         x_.append(im)
    #         y_.append(target[attr])

    return x_, y_, df_.index
    
# x = np.array([load_reshape_img(imageDirectory + fname) for fname in ['000001.jpg','000002.jpg','000003.jpg']])
# # load_reshape_img(imageDirectory+'000001.jpg')
# x = x.reshape(x.shape[0], 218, 178, 3)
# print(x.shape)


# Uncomment from here if you don't have a pretrained model
#########################################################################


inceptionModel = keras.applications.InceptionV3(include_top = False)
inceptionModel.trainable = False
# print(inceptionModel.summary())
x = inceptionModel.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(1024, activation="relu")(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(512, activation="relu")(x)
predictions = layers.Dense(2, activation="softmax")(x)
finalModel = keras.Model(inputs = inceptionModel.input, outputs = predictions)

finalModel.compile(optimizer = 'adam',
                loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
                metrics=['categorical_accuracy'])

for attr in ATTR:

    xTrain, yTrain, indexes = generate_df(parAttr,0, attr, 10000)
    xTest, yTest, indexes = generate_df(parAttr,2, attr, 1000)
    print(xTrain.shape)
    print(yTrain.shape)
    with tf.device('/gpu:0'):
        finalModel.fit(xTrain,yTrain,batch_size = 32, epochs = 1)
        finalModel.evaluate(xTest,yTest,batch_size = 32)
    finalModel.save('./' + attr)
    
#########################################################################

# Load pretrained model


# newModel.summary()
# xTest, yTest, indexes = generate_df(parAttr,1, ATTR, 100)
# newModel.evaluate(xTest,yTest,verbose = 2)


def testWithTruth(fname):
    iname = imageDirectory+str(fname)
    img = PIL.Image.open(iname)
    img.show()
    img = np.asarray(img)/255.
    for i in ATTR:
        groundTruth = keras.utils.to_categorical(attributes.loc[fname,i],2)
        # print(np.argmax(groundTruth))
        x = img.reshape((1,) + img.shape)
        Prob = newModel.predict(x)
        attrResult = 0
        result = 0
        if np.argmax(Prob) == 1:
            attrResult = 1
        if np.argmax(Prob) == np.argmax(groundTruth):
            result = 1

        if attrResult == 1:
            print("The subject has the attribute: "+ str(i))
        else:
            print("The subject does not have the attribute: "+ str(i))
        if result == 1:
            print("The prediction is correct.")
        else:
            print("The prediction is NOT correct.")
    

def test(fname):

    iname = str(fname)
    img = PIL.Image.open(iname)
    img = np.asarray(img)/255.
    for i in ATTR:

        print('Loading pretrained model, this will take a while (~30 sec to 1 min)')
        # this can be speed up by only saving and loading the weights, maybe
        newModel = tf.keras.models.load_model('./' + i,compile=False)
        print('Model loaded')

        x = img.reshape((1,) + img.shape)
        Prob = newModel.predict(x)
        print(Prob)
        attrResult = 0
        result = 0
        if np.argmax(Prob) == 1:
            attrResult = 1
        if attrResult == 1:
            print("The subject has the attribute: "+ str(i))
        else:
            print("The subject does not have the attribute: "+ str(i))

# This function randomly picks images for each attributes you set to evaluate.
def randomTest():
    for i in ATTR:
        xT, xTruth, dataFrameIndex = generate_df(parAttr,2, i, 1)
        Prob = newModel.predict(xT)
        attrResult = 0
        result = 0
        if np.argmax(Prob) == 1:
            attrResult = 1
        if np.argmax(Prob) == np.argmax(xTruth):
            result = 1
        fname = imageDirectory+str(dataFrameIndex[0])
        image = PIL.Image.open(fname)
        image.show()
        if attrResult == 1:
            print("The subject has the attribute: "+ str(i))
        else:
            print("The subject does not have the attribute: "+ str(i))
        if result == 1:
            print("The prediction is correct.")
        else:
            print("The prediction is NOT correct.")

test('IMG_5970.jpg')

# randomTest()
# testWithTruth('193508.jpg')

