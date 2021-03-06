'''
Comparing single layer MLP with deep MLP (using TensorFlow)
'''

import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from math import sqrt
import pickle
import time

# Do not change this
def initializeWeights(n_in,n_out):
    """
    # initializeWeights return the random weights for Neural Network given the
    # number of node in the input layer and output layer

    # Input:
    # n_in: number of nodes of the input layer
    # n_out: number of nodes of the output layer
                            
    # Output: 
    # W: matrix of random initial weights with size (n_out x (n_in + 1))"""
    epsilon = sqrt(6) / sqrt(n_in + n_out + 1);
    W = (np.random.rand(n_out, n_in + 1)*2* epsilon) - epsilon;
    return W



# Replace this with your sigmoid implementation
def sigmoid(z):
    return  1.0/(1.0+np.exp(-1.0 * z))
	
# Replace this with your nnObjFunction implementation
def nnObjFunction(params, *args):

    start_time = time.time()
    n_input, n_hidden, n_class, training_data, training_label, lambdaval = args

    w1 = params[0:n_hidden * (n_input + 1)].reshape((n_hidden, (n_input + 1)))
    w2 = params[(n_hidden * (n_input + 1)):].reshape((n_class, (n_hidden + 1)))
    obj_val = 0
   
    grad_w1 = np.zeros(shape=(n_hidden,n_input+1))
    grad_w2 = np.zeros(shape=(n_class,n_hidden+1))
    
    print("Inside nnScript.py")
    # Your code here
    #

    #Input to Hidden Layer - Forward Pass
    trainingDataLength = len(training_data)
    inputData = np.ones((trainingDataLength,len(training_data[0])+1))
    inputData[:,:-1] = training_data
    inputData = inputData.transpose()

    
    HiddenLayerOutput = np.dot(w1,inputData)
    HiddenLayerOutput = sigmoid(HiddenLayerOutput)

    #Hidden to Output Layer - Forward Pass
    HiddenLayerBiasAdded = np.ones((len(HiddenLayerOutput)+1,len(HiddenLayerOutput[0])))
    HiddenLayerBiasAdded[:-1,:] = HiddenLayerOutput

    OutputLayer = np.zeros(shape=(n_class,trainingDataLength))
    OutputLayer = np.dot(w2,HiddenLayerBiasAdded)
    OutputLayer = sigmoid(OutputLayer)
    #training_label = training_label.T
    #1 of K code scheme matrix
   
    OutputKSchemeMatrix = np.zeros(shape=(n_class,trainingDataLength))
    maxIndices = np.argmax(training_label,axis=1)
    for i in range(trainingDataLength):
        #print("print4 : ",training_label[i])
        #print("maxIndices : ",maxIndices[i])
        OutputKSchemeMatrix[maxIndices[i],[i]] = 1


    #error Function Val
    errorFunctionVal = -((np.multiply(np.log(OutputLayer),OutputKSchemeMatrix))+(np.multiply(np.log(1-OutputLayer),1-OutputKSchemeMatrix)))

    #summation of error Function values for all training examples
    obj_val=np.sum(errorFunctionVal)

    #Backward error propagation - Output to Hidden Layer
    HiddenLayerOutput2 = HiddenLayerBiasAdded.transpose()
    grad_w2=np.dot((OutputLayer-OutputKSchemeMatrix),HiddenLayerOutput2)

    #Backward error propagation - Hidden Layer to Input Layer
    transpose_w2 = w2.transpose()
    transpose_w2 = np.delete(transpose_w2,(n_hidden), axis=0)
    inputData = inputData.transpose()
    scalarMul = np.multiply(1-HiddenLayerOutput,HiddenLayerOutput)
    deltaScalarMul = scalarMul*np.dot(transpose_w2,OutputLayer-OutputKSchemeMatrix)
    
    grad_w1=(np.dot(deltaScalarMul,inputData))

    obj_val = obj_val/trainingDataLength
    
    #Compute InputToHiddenSum and HiddenToOutputSum to calculate regularization that should be added to object value
    InputToHiddenSum=np.sum(w1**2)
    HiddenToOutputSum=np.sum(w2**2)
        
    obj_val+=((lambdaval/(2*trainingDataLength))*(InputToHiddenSum+HiddenToOutputSum))

    #Adding regularization terms for grad_w1 and grad_w2
    grad_w2+=lambdaval*w2
    grad_w2=grad_w2/trainingDataLength

    grad_w1+=lambdaval*w1
    grad_w1/=trainingDataLength           
        
    print("obj_val",obj_val)
    
    # Make sure you reshape the gradient matrices to a 1D array. for instance if your gradient matrices are grad_w1 and grad_w2
    # you would use code similar to the one below to create a flat array
    #print("grad_w1 ",len(grad_w1)*len(grad_w1[0]))
    #print("grad_w2 ",len(grad_w2)*len(grad_w2[0]))
    obj_grad = np.array([])
    obj_grad = np.concatenate((grad_w1.flatten(), grad_w2.flatten()),0)
    
    #print(len(obj_grad))
    print("obj_grad",obj_grad)
    end_time = time.time()
    print("Time taken : ",end_time-start_time)
    return (obj_val, obj_grad)
    
# Replace this with your nnPredict implementation
def nnPredict(w1,w2,data):
    # Your code here
    
    predictDataLength = len(data)
    labels = np.zeros(shape=(predictDataLength,2))
    inputData = np.ones((predictDataLength,len(data[0])+1))
    inputData[:,:-1] = data
    inputData = inputData.transpose()

    HiddenLayerOutput = np.dot(w1,inputData)
    HiddenLayerOutput = sigmoid(HiddenLayerOutput)

    #Hidden to Output Layer - Forward Pass
    HiddenLayerBiasAdded = np.ones((len(HiddenLayerOutput)+1,len(HiddenLayerOutput[0])))
    HiddenLayerBiasAdded[:-1,:] = HiddenLayerOutput

    OutputLayer = np.zeros(shape=(2,predictDataLength))
    OutputLayer = np.dot(w2,HiddenLayerBiasAdded)
    OutputLayer = sigmoid(OutputLayer)

    #Find maximum from each row
    max_labels = np.argmax(OutputLayer.transpose(),axis=1)
  
    for i in range(predictDataLength):
        labels[i,max_labels[i]] = 1
  
    print(labels)
    return labels

# Do not change this
def preprocess():
    pickle_obj = pickle.load(file=open('face_all.pickle', 'rb'))
    features = pickle_obj['Features']
    labels = pickle_obj['Labels']
    train_x = features[0:21100] / 255
    valid_x = features[21100:23765] / 255
    test_x = features[23765:] / 255
    labels = labels[0]
    train_y = np.zeros(shape=(21100, 2))
    train_l = labels[0:21100]
    valid_y = np.zeros(shape=(2665, 2))
    valid_l = labels[21100:23765]
    test_y = np.zeros(shape=(2642, 2))
    test_l = labels[23765:]
    for i in range(train_y.shape[0]):
        train_y[i, train_l[i]] = 1
    for i in range(valid_y.shape[0]):
        valid_y[i, valid_l[i]] = 1
    for i in range(test_y.shape[0]):
        test_y[i, test_l[i]] = 1

    return train_x, train_y, valid_x, valid_y, test_x, test_y
"""**************Neural Network Script Starts here********************************"""
train_data, train_label, validation_data, validation_label, test_data, test_label = preprocess()
#  Train Neural Network
# set the number of nodes in input unit (not including bias unit)
n_input = train_data.shape[1]
# set the number of nodes in hidden unit (not including bias unit)
n_hidden = 256
# set the number of nodes in output unit
n_class = 2

# initialize the weights into some random matrices
initial_w1 = initializeWeights(n_input, n_hidden);
initial_w2 = initializeWeights(n_hidden, n_class);
# unroll 2 weight matrices into single column vector
initialWeights = np.concatenate((initial_w1.flatten(), initial_w2.flatten()),0)
# set the regularization hyper-parameter
lambdaval = 10;
args = (n_input, n_hidden, n_class, train_data, train_label, lambdaval)

#Train Neural Network using fmin_cg or minimize from scipy,optimize module. Check documentation for a working example
opts = {'maxiter' :50}    # Preferred value.

nn_params = minimize(nnObjFunction, initialWeights, jac=True, args=args,method='CG', options=opts)
params = nn_params.get('x')
#Reshape nnParams from 1D vector into w1 and w2 matrices
w1 = params[0:n_hidden * (n_input + 1)].reshape( (n_hidden, (n_input + 1)))
w2 = params[(n_hidden * (n_input + 1)):].reshape((n_class, (n_hidden + 1)))

#Test the computed parameters
predicted_label = nnPredict(w1,w2,train_data)
#find the accuracy on Training Dataset
print('\n Training set Accuracy:' + str(100*np.mean((predicted_label == train_label).astype(float))) + '%')
predicted_label = nnPredict(w1,w2,validation_data)
#find the accuracy on Validation Dataset
print('\n Validation set Accuracy:' + str(100*np.mean((predicted_label == validation_label).astype(float))) + '%')
predicted_label = nnPredict(w1,w2,test_data)
#find the accuracy on Validation Dataset
print('\n Test set Accuracy:' +  str(100*np.mean((predicted_label == test_label).astype(float))) + '%')
