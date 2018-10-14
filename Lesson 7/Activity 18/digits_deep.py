import tensorflow.keras.datasets.mnist as mnist 
import numpy as np 
import tensorflow as tf
import random
from sklearn.metrics import accuracy_score

# Import and preprocess data
(featuresTrain, labelTrain),(featuresTest, labelTest) = mnist.load_data() 

featuresTrain = featuresTrain / 255.0 
featuresTest = featuresTest / 255.0 

def flatten(matrix):  
    return [ elem for row in matrix for elem in row ] 

featuresTrainVector = [  
    flatten(image) for image in featuresTrain  
] 
featuresTestVector = [  
    flatten(image) for image in featuresTest  
] 

labelTrainVector = np.zeros((labelTrain.size, 10)) 
for i, label in enumerate( labelTrainVector ): 
    label[ labelTrain[i] ] = 1 
labelTestVector = np.zeros((labelTest.size, 10)) 
for i, label in enumerate( labelTestVector ): 
    label[ labelTest[i] ] = 1

# Set up the TensorFlow graph
x = tf.placeholder( tf.float32, [None, 28 * 28 ] ) 
f1 = tf.nn.relu 
W1 = tf.Variable( tf.random_normal( [784, 200] ) ) 
b1 = tf.Variable( tf.random_normal( [200] ) ) 
layer1Out = f1( tf.add( tf.matmul( x, W1 ), b1 ) ) 
f2 = tf.nn.softmax 
W2 = tf.Variable( tf.random_normal([200, 100])) 
b2 = tf.Variable( tf.random_normal( [100] ) ) 
layer2Out = f2( tf.add( tf.matmul( layer1Out, W2 ), b2 ) ) 
f3 = tf.nn.softmax 
W3 = tf.Variable( tf.random_normal( [100, 10] ) ) 
b3 = tf.Variable( tf.random_normal( [10] ) ) 
y = f3( tf.add( tf.matmul( layer2Out, W3 ), b3 ) )

# Train the model
y_true = tf.placeholder( tf.float32, [None, 10] ) 
crossEntropy = tf.nn.softmax_cross_entropy_with_logits_v2( 
    logits=y,  
    labels=y_true 
) 

cost = tf.reduce_mean( crossEntropy ) 
optimizer = tf.train.GradientDescentOptimizer( learning_rate = 0.5 ).minimize( cost ) 

session = tf.Session() 
session.run( tf.global_variables_initializer() ) 

iterations = 600 
batchSize = 200 
sampleSize = len( featuresTrainVector ) 

for _ in range( iterations ): 
    indices = random.sample( range(sampleSize), batchSize ) 
    batchFeatures = [  
        featuresTrainVector[i] for i in indices 
    ] 
    batchLabels = [ 
        labelTrainVector[i] for i in indices 
    ] 
    min = i * batchSize 
    max = (i+1) * batchSize 
    dictionary = {  
        x: batchFeatures, 
        y_true: batchLabels 
    } 
    session.run( optimizer, feed_dict=dictionary ) 

labelPredicted = session.run( y, feed_dict={ 
    x: featuresTestVector 
} ) 

labelPredicted = [  
    np.argmax(label) for label in labelPredicted  
] 

print(
    'Confusion matrix:',
    confusion_matrix( labelTest, labelPredicted )
)

print(
    'Accuracy score:',
    accuracy_score( labelTest, labelPredicted )
)