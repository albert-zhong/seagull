import numpy as np


class GradientDescent:
    def __init__(self, X, y, alpha=0.01, iterations=100):  # by default alpha=0.01 and iterations=100
        self.X = X
        self.y = y

        self.m, self.n = X.shape  # m is the number of training examples, n is the number of features
        # n > 1 since we will always have "1" as the first feature to allow for bias calculation

        self.theta = np.ones(self.n)  # parameters for the predictive function that will soon be made
        self.alpha = alpha  # alpha is the learning rate
        self.iterations = iterations

    def train(self):
        for i in range(self.iterations):
            hypothesis = np.dot(self.X, self.theta)
            loss = hypothesis - self.y
            gradient = np.dot(self.X.transpose(), loss) / self.m
            self.theta -= self.alpha * gradient

    def predict(self, x):
        return np.dot(self.theta, x)
