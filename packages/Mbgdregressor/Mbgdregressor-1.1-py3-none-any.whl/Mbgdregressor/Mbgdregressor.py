"""Linear model fitted by minimizing a empirical loss with MBGD.

MBGD stands for Mini Batch Gradient Descent: the gradient of the loss is
estimated by each batch at a time and the model is updated along the way with
a decreasing strength schedule (aka learning rate).

This implementation works with data represented as dense numpy arrays of
floating point values for the features.

Parameters
----------
batch_size: int 
    constant that fixes the batch size for number of updates in each epoch.
learning_rate: float default = 0.01
epochs: int default = 100
    constant that fixes number of iteration.

Attributes
----------
coef_ : ndarray of shape (n_features,)
    Weights assigned to the features.
intercept_ : ndarray of shape (1,)
    The intercept term.

Examples
--------
>>> import numpy as np
>>> import Mbgdregressor
>>> from sklearn.datasets import load_diabetes

>>> X,y = load_diabetes(return_X_y=True)
>>> X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=2)
>>> batch = X_train.shape[0]//20
>>> model = Mbgdregressor(batch_size= batch,learning_rate=0.01,epochs=100)
>>> model.fit(X_train,y_train)
>>> y_pred = model.predict(X_test)
"""
import random
import numpy as np


class Mbgdregressor:

    def __init__(self, batch_size, learning_rate=0.01, epochs=100):

        self.coef_ = None
        self.intercept_ = None
        self.lr = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size

    def fit(self, X_train, y_train):
        # init your coefs
        self.intercept_ = 0
        self.coef_ = np.ones(X_train.shape[1])

        for i in range(self.epochs):

            for j in range(int(X_train.shape[0]/self.batch_size)):

                idx = random.sample(range(X_train.shape[0]), self.batch_size)

                y_hat = np.dot(X_train[idx], self.coef_) + self.intercept_
                intercept_der = -2 * np.mean(y_train[idx] - y_hat)
                self.intercept_ = self.intercept_ - (self.lr * intercept_der)

                coef_der = -2 * np.dot((y_train[idx] - y_hat), X_train[idx])
                self.coef_ = self.coef_ - (self.lr * coef_der)

        print(self.intercept_, self.coef_)

    def predict(self, X_test):
        return np.dot(X_test, self.coef_) + self.intercept_
