import numpy
import pandas
import math
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

numpy.random.seed(7)

dataframe = numpy.loadtxt("Kingston_Police_Formatted.csv",delimiter=",")
train_size = int(len(dataframe)*0.67)
test_size = int(len(dataframe)-train_size)

train_main, test_main = dataframe[0:train_size,9:], dataframe[train_size:len(dataframe),9:]

def create_database(dataset,look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a= dataset[i:(i+look_back),:]
        dataX.append(a)
        dataY.append(dataset[i+look_back,:])
    return numpy.array(dataX), numpy.array(dataY)


trainX_main, trainY_main = create_database(train_main,4)
testX_main, testY_main = create_database(test_main,4)

trainX_main = numpy.reshape(trainX_main,(trainX_main.shape[0],4,2))
testX_main = numpy.reshape(testX_main,(testX_main.shape[0],4,2))



model=Sequential()
model.add(LSTM(32,input_dim=2))
model.add(Dense(2))
model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(trainX_main, trainY_main, nb_epoch=10,batch_size=10, verbose=2)

score = model.evaluate(testX_main,testY_main,batch_size=10)

print(score)

model.save('my_modeltest.h5')
