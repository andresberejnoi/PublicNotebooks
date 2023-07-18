"Collection of activations functions for the neural network"

import numpy as np


# define some activation and error functions
def tanh(x, derivative=False):
    """Implements the hyperbolic tangent function element wise over an array x.

    Parameters
    ----------
    x : numpy array
        This array contains arguments for the hyperbolic tangent function.
    derivative : bool
        Indicates whether to use the hyperbolic tangent function or its derivative.

    Returns
    -------
    numpy array
        An array of equal shape to `x`.
    """

    if derivative:
        tanh_not_derivative = tanh(x)
        return 1.0 - tanh_not_derivative**2
        #return 1.0 - x**2
    else:
        return np.tanh(x)

def relu(x, derivative=False):
    if derivative:
        return 1 * (x > 0)  #returns 1 for any x > 0, and 0 otherwise
    
    return np.maximum(0, x)

def softmax(x, derivative=False):
    if derivative:
        pass
    
    return np.exp(x)/sum(np.exp(x)) 

def softmax_grad(softmax):
    # https://stackoverflow.com/questions/40575841/numpy-calculate-the-derivative-of-the-softmax-function
    # https://stackoverflow.com/questions/33541930/how-to-implement-the-softmax-derivative-independently-from-any-loss-function
    #
    
    # Reshape the 1-d softmax to 2-d so that np.dot will do the matrix multiplication
    s = softmax.reshape(-1,1)
    return np.diagflat(s) - np.dot(s, s.T)

def mean_squared_error(target_output, actual_output, derivative=False):
    try:
        assert(target_output.shape == actual_output.shape)
    except AssertionError:
        print(f"Shape of target vector: {target_output.shape} does not match shape of actual vector: {actual_output.shape}")
    if derivative:
        error = (actual_output - target_output)
    
    else:
        error = np.sum(0.5 * np.sum((target_output-actual_output)**2, axis=1, keepdims=True))
        
    return error
