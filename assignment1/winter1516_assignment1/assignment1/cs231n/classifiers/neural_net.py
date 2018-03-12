import numpy as np
import matplotlib.pyplot as plt


class TwoLayerNet(object):
  """
  A two-layer fully-connected neural network. The net has an input dimension of
  N, a hidden layer dimension of H, and performs classification over C classes.
  We train the network with a softmax loss function and L2 regularization on the
  weight matrices. The network uses a ReLU nonlinearity after the first fully
  connected layer.

  In other words, the network has the following architecture:

  input - fully connected layer - ReLU - fully connected layer - softmax

  The outputs of the second fully-connected layer are the scores for each class.
  """

  def __init__(self, input_size, hidden_size, output_size, std=1e-4):
    """
    Initialize the model. Weights are initialized to small random values and
    biases are initialized to zero. Weights and biases are stored in the
    variable self.params, which is a dictionary with the following keys:

    W1: First layer weights; has shape (D, H)
    b1: First layer biases; has shape (H,)
    W2: Second layer weights; has shape (H, C)
    b2: Second layer biases; has shape (C,)

    Inputs:
    - input_size: The dimension D of the input data.
    - hidden_size: The number of neurons H in the hidden layer.
    - output_size: The number of classes C.
    """
    self.params = {}
    self.params['W1'] = std * np.random.randn(input_size, hidden_size)
    self.params['b1'] = np.zeros(hidden_size)
    self.params['W2'] = std * np.random.randn(hidden_size, output_size)
    self.params['b2'] = np.zeros(output_size)

  def loss(self, X, y=None, reg=0.0):
    """
    Compute the loss and gradients for a two layer fully connected neural
    network.

    Inputs:
    - X: Input data of shape (N, D). Each X[i] is a training sample.
    - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
      an integer in the range 0 <= y[i] < C. This parameter is optional; if it
      is not passed then we only return scores, and if it is passed then we
      instead return the loss and gradients.
    - reg: Regularization strength.

    Returns:
    If y is None, return a matrix scores of shape (N, C) where scores[i, c] is
    the score for class c on input X[i].

    If y is not None, instead return a tuple of:
    - loss: Loss (data loss and regularization loss) for this batch of training
      samples.
    - grads: Dictionary mapping parameter names to gradients of those parameters
      with respect to the loss function; has the same keys as self.params.
    """
    # Unpack variables from the params dictionary
    W1, b1 = self.params['W1'], self.params['b1']
    W2, b2 = self.params['W2'], self.params['b2']
    #W3, b3 = self.params['W3'], self.params['b3']

    N, D = X.shape

    # Compute the forward pass
    scores = None
    #############################################################################
    # TODO: Perform the forward pass, computing the class scores for the input. #
    # Store the result in the scores variable, which should be an array of      #
    # shape (N, C).                                                             #
    #############################################################################
   
    
    l1 = X.dot(W1)+ b1.T
    l2 = l1*(l1>0) # ReLu
    l3 = l2.dot(W2)+ b2.T
    #l4 = l3*(l3>0) # ReLu
    #l5 = l4.dot(W3)+ b3.T
 
    scores = l3 
    # If the targets are not given then jump out, we're done
    if y is None:
      return scores

    # Compute the loss
    loss = None
    #############################################################################
    # TODO: Finish the forward pass, and compute the loss. This should include  #
    # both the data loss and L2 regularization for W1 and W2. Store the result  #
    # in the variable loss, which should be a scalar. Use the Softmax           #
    # classifier loss. So that your results match ours, multiply the            #
    # regularization loss by 0.5                                                #
    #############################################################################

    #sumExp = np.sum(np.exp(l5), axis=1)
    #l6 = np.sum(-l5[range(N), y]+np.log(sumExp) ) / N
    sumExp = np.sum(np.exp(l3), axis=1)
    l4 = np.sum(-l3[range(N), y]+np.log(sumExp) ) / N
    
    
    # regularization
    #loss =l6+ 0.5 * reg *  (np.sum(W1*W1) + np.sum(W2*W2) )#+ np.sum(W3*W3))
    loss =l4+ 0.5 * reg *  (np.sum(W1*W1) + np.sum(W2*W2) )#+ np.sum(W3*W3))
    
    #############################################################################

    # Backward pass: compute gradients
    grads = {}
    #############################################################################
    # TODO: Compute the backward pass, computing the derivatives of the weights #
    # and biases. Store the results in the grads dictionary. For example,       #
    # grads['W1'] should store the gradient on W1, and be a matrix of same size #
    #############################################################################

    
    #correct_class_score = np.exp(scores[np.arange(N), y])
    #loss = np.mean(-np.log(correct_class_score/sumExp ))
    '''
    dl6 = 1.00
    ind = np.zeros(l5.shape)
    ind[np.arange(N), y] = 1
    dL5 = (np.exp(l5).T/sumExp).T - ind
    dL5 /= N
    
    dL4 = dL5.dot(W3.T)
    
    dL3 = dL4*((l3>0))

    
    '''
    dl4 = 1.00
    ind = np.zeros(l3.shape)
    ind[np.arange(N), y] = 1
    dL3 = (np.exp(l3).T/sumExp).T - ind
    dL3 /= N
    
    dL2 = dL3.dot(W2.T)

    dL1 = dL2*((l1>0))

    dW1 = (X.T).dot(dL1)
    db1 = np.sum(dL1, axis=0)
    dW2 = l2.T.dot(dL3)
    db2 = np.sum(dL3, axis=0)
    #dW3 = l4.T.dot(dL5)
    #db3 = np.sum(dL5, axis=0) 
   
    # regularization
    dW1 += reg * W1
    dW2 += reg * W2
    #dW3 += reg * W3

    grads['W1'] = dW1
    grads['W2'] = dW2
    #grads['W3'] = dW3
    grads['b1'] = db1
    grads['b2'] = db2
    #grads['b3'] = db3

    return loss, grads

  def train(self, X, y, X_val, y_val,
            learning_rate=1e-3, learning_rate_decay=0.95,
            reg=1e-5, num_iters=100,
            batch_size=200, verbose=False, isRand=True):
    """
    Train this neural network using stochastic gradient descent.

    Inputs:
    - X: A numpy array of shape (N, D) giving training data.
    - y: A numpy array f shape (N,) giving training labels; y[i] = c means that
      X[i] has label c, where 0 <= c < C.
    - X_val: A numpy array of shape (N_val, D) giving validation data.
    - y_val: A numpy array of shape (N_val,) giving validation labels.
    - learning_rate: Scalar giving learning rate for optimization.
    - learning_rate_decay: Scalar giving factor used to decay the learning rate
      after each epoch.
    - reg: Scalar giving regularization strength.
    - num_iters: Number of steps to take when optimizing.
    - batch_size: Number of training examples to use per step.
    - verbose: boolean; if true print progress during optimization.
    """
    num_train = X.shape[0]
    iterations_per_epoch = 50 #np.floor(max(num_train / batch_size, 1))
    print('epoch: ', iterations_per_epoch)
    

    # Use SGD to optimize the parameters in self.model
    loss_history = []
    train_acc_history = []
    val_acc_history = []

    for it in range(num_iters):
        if isRand==True:
            batchNum = np.random.choice(num_train, batch_size, replace=False)
            X_batch = X[batchNum,:]
            y_batch = y[batchNum]
     
        else:
          #  if it*batch_size+batch_size-1>num_train:
          #      break
                
            stIdx = max(it*batch_size% num_train, 0)
            edIdx = min(stIdx+batch_size-1, num_train)
            batchNum = range(stIdx, edIdx)
            X_batch = X[batchNum,:]
            y_batch = y[batchNum]
            #print(batchNum)    

        
        # Compute loss and gradients using the current minibatch
        loss, grads = self.loss(X_batch, y=y_batch, reg=reg)
        loss_history.append(loss)

        
        self.params['W1'] -= learning_rate * grads['W1']
        self.params['b1'] -= learning_rate * grads['b1']
        self.params['W2'] -= learning_rate * grads['W2']
        self.params['b2'] -= learning_rate * grads['b2']

        #########################################################################
        # TODO: Use the gradients in the grads dictionary to update the         #
        # parameters of the network (stored in the dictionary self.params)      #
        # using stochastic gradient descent. You'll need to use the gradients   #
        # stored in the grads dictionary defined above.                         #
        #########################################################################
      
        if verbose and it % iterations_per_epoch == 0:
            print ('iteration %d / %d: loss %f' % (it, num_iters, loss))

        # Every epoch, check train and val accuracy and decay learning rate.
        if it % iterations_per_epoch == 0:
            # Check accuracy
            train_acc = np.mean(self.predict(X_batch) == y_batch)
            val_acc = np.mean(self.predict(X_val) == y_val)
            train_acc_history.append(train_acc)
            val_acc_history.append(val_acc)

            # Decay learning rate
            learning_rate *= learning_rate_decay

    return {
        'loss_history': loss_history,
        'train_acc_history': train_acc_history,
        'val_acc_history': val_acc_history,
    }

  def predict(self, X):
    """
    Use the trained weights of this two-layer network to predict labels for
    data points. For each data point we predict scores for each of the C
    classes, and assign each data point to the class with the highest score.

    Inputs:
    - X: A numpy array of shape (N, D) giving N D-dimensional data points to
      classify.

    Returns:
    - y_pred: A numpy array of shape (N,) giving predicted labels for each of
      the elements of X. For all i, y_pred[i] = c means that X[i] is predicted
      to have class c, where 0 <= c < C.
    """
   
 
    l1 = X.dot(self.params['W1'])+ self.params['b1'].T
    l2 = l1*(l1>0) # ReLu
    l3 = l2.dot(self.params['W2'])+ self.params['b2'].T
     
    scores = l3 
    sumExp = np.sum(np.exp(l3), axis=1)
    #   scores = -np.log(np.exp(l3)/sumExp)
    
   
    
    y_pred = np.argmax(scores, axis = 1)
   
    ###########################################################################
    # TODO: Implement this function; it should be VERY simple!                #
    ###########################################################################

    return y_pred


