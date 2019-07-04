import numpy as np


class GradientDescent(object):
    def __init__(self, X, y, alpha=0.01, iterations=100):  # by default alpha=0.01 and iterations=100
        self.X = X
        self.y = y

        self.m, self.n = X.shape

        self.theta = np.ones(self.n)  # parameters for the predictive function that will soon be made
        self.alpha = alpha  # alpha is the learning rate
        self.iterations = iterations

    def learn(self):
        for i in range(self.iterations):
            hypothesis = np.dot(self.X, self.theta)
            loss = hypothesis - self.y
            gradient = np.dot(self.X.transpose(), loss) / self.m
            self.theta -= self.alpha * gradient


X = np.array([[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]])
y = np.array([2, 3, 4, 5, 6])

test = GradientDescent(X, y)
test.learn()
print(test.theta)