# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import backend as K


# %%
####################################
## Functions
####################################

def load_reshape_img(fname):
    '''
    Takes an image file name/location, reads and processes the image using keras, and finally reshapes the image. 
    This reshaped image is then returned.
    '''

    # Load image as PIL format
    img = keras.preprocessing.image.load_img(fname)
    # Convert image to np array and normalize
    x = keras.preprocessing.image.img_to_array(img)/255.
    # x = x.astype(np.uint8)
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

    # The sample size is at most the number stated above, but at least the size of the smallest class of the dataframe. 
    # This results in some uncommon attributes (e.g. sideburns) having to train on very few samples.
    min_class_size=min(len(df[(df['partition'] == partition) & (df[attr] == 0)]),len(df[(df['partition'] == partition) & (df[attr] == 1)]) )
    sample_size=int(num_samples/2)
    if(min_class_size<int(num_samples/2)):
        sample_size=min_class_size
    
    df_ = df[(df['partition'] == partition) & (df[attr] == 0)].sample(sample_size)
    df_ = pd.concat([df_, df[(df['partition'] == partition) & (df[attr] == 1)].sample(sample_size)])


    # sample desired amount of images of input partition
    # df_ = df[(df['partition'] == partition)].sample(num_samples)
    # print(df_)

    x_ = np.array([load_reshape_img(imageDirectory + fname) for fname in df_.index])
    # reshape into shape of [# of samples, 218, 178, 3]
    x_ = tf.convert_to_tensor(x_.reshape(x_.shape[0], 218, 178, 3))
    # one-hot encode the y values
    y_ = tf.convert_to_tensor(keras.utils.to_categorical(df_[attr],2))
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

def loadModel(attribute):
    '''
    This function loads a pretrained model. It takes the attribute name associated with the model as a string
    and returns the loaded model.
    '''
    model = createModel(0)
    # expect_partial() is needed to silence warnings about incomplete checkpoint restores
    # A lot of variables are unused when just predicting, tensorflow prints a warning for each variable you don't use
    model.load_weights('./models/'+str(attribute)+' Model').expect_partial()
    return model

def createModel(compileEnable):
    '''
    This function creates the model structure to be trained with our labeled data. It utilizes the keras pretrained
    inception model and adds some final layers to be trained on top of with out labeled data.
    '''
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

    if compileEnable == 1:
        finalModel.compile(optimizer = 'adam',
                        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
                        metrics=['categorical_accuracy'])
        return finalModel
    else:
        return finalModel

def testWithTruth(index,fname):
    model = loadModel(ATTR[index])
    iname = imageDirectory+str(fname)
    img = PIL.Image.open(iname)
    img = np.asarray(img)/255.
    groundTruth = keras.utils.to_categorical(attributes.loc[fname,ATTR[index]],2)
    # print(np.argmax(groundTruth))
    x = img.reshape((1,) + img.shape)
    # predict_step() is used now
    # First, predict() is used to predict a bunch of samples in certain amount of batches.
    # it also has its own tf.function which was causing retracing warning when used in a loop
    # not sure what tf.function does yet, but using predict_step() fixed the warning.
    Prob = model.predict_step(tf.convert_to_tensor(x))
    attrResult = 0
    result = 0
    if np.argmax(Prob) == 1:
        attrResult = 1
    if np.argmax(Prob) == np.argmax(groundTruth):
        result = 1

    if attrResult == 1:
        print("The subject has the attribute: "+ str(ATTR[index]))
    else:
        print("The subject does not have the attribute: "+ str(ATTR[index]))
    if result == 1:
        print("The prediction is correct.")
    else:
        print("The prediction is NOT correct.")

def test(index,fname):
    model = loadModel(ATTR[index])
    iname = imageDirectory+str(fname)
    img = PIL.Image.open(iname)
    img = np.asarray(img)/255.
    x = img.reshape((1,) + img.shape)
    Prob = model.predict_step(tf.convert_to_tensor(x))
    attrResult = 0
    if np.argmax(Prob) == 1:
        attrResult = 1
    if attrResult == 1:
        print("The subject has the attribute: "+ str(ATTR[index]))
    else:
        print("The subject does not have the attribute: "+ str(ATTR[index]))

def classify(fname,model):
    '''
    This function takes an image name/location as a string as well as a trained model of a certain attribute. The image
    is then read and evaluated in the model. The classification is then returned as a 1 or 0
    '''
    iname = str(fname)
    img = PIL.Image.open(iname)
    img = np.asarray(img)/255.   

    x = img.reshape((1,) + img.shape)
    Prob = model.predict_step(tf.convert_to_tensor(x))
    attrResult = 0
    if np.argmax(Prob) == 1:
        attrResult = 1
    else:
        attrResult = 0
    
    return attrResult


# %%
###########################
## Classes
###########################

class Person:
    def __init__(self, name,ID):
        self.name = name
        self.ID = ID
        self.Male = 0
        self.Eyeglasses = 0
        self.Wearing_hat = 0
        self.Smiling = 0
        self.Blond_Hair = 0

class Attribute:
    def __init__(self, name):
        self.name = name
        self.num  = 0


# %%
###########################
## Setup
###########################

# comment these off if giving you error
physicalDevices = tf.config.list_physical_devices('GPU')
# print(physicalDevices)
tf.config.experimental.set_memory_growth(physicalDevices[0],True)

## To use more than one attributes, we will do the same number of 2 class classification over all attributes
#what characteristic are we going to train and test for? (note if set to 'all' it'll use all of them)
ATTR='Blond_Hair','Eyeglasses','Male','Smiling','Wearing_Hat'

# set up working directory
currentWorkingDirectory = os.getcwd()
imageDirectory = os.path.join(currentWorkingDirectory,"CelebA\\Img\\img_align_celeba\\") 
attributesDirectory = os.path.join(currentWorkingDirectory,"CelebA\\Anno\\list_attr_celeba.csv") 
partitionsDirectory = os.path.join(currentWorkingDirectory,"CelebA\\Eval\\list_eval_partition.csv") 
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
else:
    ATTR=list(ATTR)

# modify the partitions file so that the index is the name of the image
# print(partitions['partition'].value_counts().sort_index())
partitions.set_index('image_id', inplace=True)


parAttr = partitions.join(attributes[ATTR], how='inner')
# print(parAttr.shape)


# %%
###########################
## Train the Models
###########################

# Uncomment from here if you don't have a pretrained model
#########################################################################
# trainingModel = createModel(1)
# for i in ATTR:
#     print('Training network for : '+i)
#     print('Loading training data')
#     xTrain, yTrain, indexes = generate_df(parAttr,0, i, 160000)
#     print('Loading testing data')
#     xTest, yTest, indexes = generate_df(parAttr,2, i, 19000)
#     print('Begin fitting')
#     with tf.device('/gpu:0'):
#         trainingModel.fit(xTrain,yTrain,batch_size = 32, epochs = 10)
#         print('Result evaluation')
#         trainingModel.evaluate(xTest,yTest,batch_size = 32)
#     trainingModel.save_weights('./models/'+str(i)+' Model')
#########################################################################


# %%
###########################
## Classify Images
###########################

# People objects
nathaniel = Person('Nathaniel')
sarah = Person('Sarah')
lin = Person('Lin')
xinran = Person('Xinran')
david = Person('David')
mom = Person("Sarah's Mom")
roommate = Person("Sarah's Roomate")
nick = Person('Nick')
people = [nathaniel,sarah,lin,xinran,david,mom,roommate,nick]

# Attributes
ATTR = [Attribute('Male'),Attribute('Eyeglasses'),Attribute('Wearing_Hat'),Attribute('Smiling'),Attribute('Blond_Hair')]

# Classify each image

for attr in ATTR:
    # Load the model
    print('Loading pretrained model, this will take a while (~30 sec to 1 min)')
    # this can be speed up by only saving and loading the weights, maybe
    newModel = loadModel(attr.name)
    print('Model loaded')

    for person in people:
        result = classify(person.ID,newModel)
        if result == 1:
            attr.num += 1                   # Increase the number of times attribute has occured
            setattr(person,attr.name,1)     # Set attribute of current person to 1/true


# %%
###########################
## Play the Game
###########################

done = False
while not done:

    if len(pictures) == 1:
        print('The person is ' + pictures[0])
        done = True
    elif len(ATTR) == 0:
        num = rand.choice(range(len(pictures)))
        pic = pictures.pop(num)
        text = input('Is the person ' + pic + '?' + '(y/n)\n')
        if text == 'y':
            print('The person is ' + pic)
        else:
            continue
        

    # Select the Attribute
    num = rand.choice(range(len(ATTR)))
    attribute = ATTR.pop(num)

    print('Loading pretrained model, this will take a while (~30 sec to 1 min)')
    # this can be speed up by only saving and loading the weights, maybe
    newModel = tf.keras.models.load_model('./' + attribute,compile=False)
    print('Model loaded')

    # Que the user for clue
    text = input('Does the user have the attribute ' + attribute + '(y/n):\n')
    if text == 'y':
        ans = 1
    else:
        ans = 0

    # Evaluate each picture
    for pic in pictures:
        result = test(pic,newModel)
        if ans != result:
            pictures.remove(pic)


