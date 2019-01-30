import os
import sys
import struct
import numpy as np

from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import SGD
"""
Loosely inspired by http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py
which is GPL licensed.
"""

sys.path.insert(0,r'C:\Users\amrul\Documents\programming\deep_learning\facial-expression-recognition\facial-expression-recognition-master')

# from ann import ANN

def read(dataset = "training", path = "."):
    """
    Python function for importing the MNIST data set.  It returns an iterator
    of 2-tuples with the first element being the label and the second element
    being a numpy.uint8 2D array of pixel data for the given image.
    """

    if dataset is "training":
        fname_img = os.path.join(path, 'train-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels-idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)

    get_img = lambda idx: (lbl[idx], img[idx])

    # Create an iterator which returns each image in turn
    for i in range(len(lbl)):
        yield get_img(i)

def show(image):
    """
    Render a given numpy.uint8 2D array of pixel data.
    """
    from matplotlib import pyplot
    import matplotlib as mpl
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    pyplot.show()

itr=read(dataset='training',path="C:\\Users\\amrul\\Downloads\\codes\\mnist_dataset\\")


X=[]
T=[]
for i in range(3000):
    tpl_lbl,tpl_img=next(itr)
    T.append(tpl_lbl)
    X.append(tpl_img.reshape(784,))

X=np.array(X)
T=np.array(T)
#build, compile and fit the model
target=to_categorical(T)
model2=Sequential()
model2.add(Dense(100,activation='relu',input_shape=(X.shape[1],)))
model2.add(Dense(100,activation='relu'))
model2.add(Dense(10,activation='softmax'))
my_optimizer=SGD(0.01)
model2.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
model2.fit(X,target,epochs=100)
# model=ANN(200)
# model.fit(X,T,reg=0,show_fig=True)
# print(model.score(X,T))