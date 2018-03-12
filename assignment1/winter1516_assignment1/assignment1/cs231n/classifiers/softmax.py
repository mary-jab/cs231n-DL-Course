import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  N = X.shape[0]
  C = W.shape[1]
  for i in range(N):
        scores = X[i].dot(W)
        mx = np.max(scores)
        scores -= mx
        correct_class_score = scores[y[i]]
        
        sumExp = np.sum(np.exp(scores))
        loss += -correct_class_score + np.log(sumExp)

        for j in range(C):
            p = np.exp(scores[j])/sumExp
            
            if j != y[i]:
                dW[:,j] += X[i]* p 
            else:
                dW[:,j] +=X[i]*(p-1)
            
  
  # regularization
  dW /= N
  dW += reg*W
  loss /=N
  loss += 0.5 * reg * np.sum(W * W)
 
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  pass
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    N = X.shape[0]
    C = W.shape[1]

    scores = X.dot(W)
    mx = np.max(scores, axis=1)
    scores = scores.T  
    scores -= mx
    sumExp = np.sum(np.exp(scores), axis=0)
    scores = scores.T  
    
    #correct_class_score = np.exp(scores[np.arange(N), y])
    #loss = np.mean(-np.log(correct_class_score/sumExp ))
    
    p = np.exp(scores.T)/sumExp
    p = p.T
    
    loss = np.mean(-np.log( p[np.arange(N), y] ))

    
    ind = np.zeros(p.shape)
    ind[np.arange(N), y] = 1

    
    dW =  (X.T).dot(p-ind)
  
    # regularization
    dW /= N
    dW += reg*W
    loss += 0.5 * reg * np.sum(W * W)
  
    return loss, dW

