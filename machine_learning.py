import random

class LinearRegression:
    """
    A simple Linear Regression model for predicting numerical outputs.
    """
    def __init__(self):
        self.weights = []
        self.bias = 0

    def train(self, data, learning_rate=0.01, epochs=1000):
        """
        Trains the model using gradient descent.
        :param data: List of tuples [(features, target)], where features is a list of numerical values and target is a numerical value.
        :param learning_rate: Learning rate for gradient descent.
        :param epochs: Number of training iterations.
        """
        num_features = len(data[0][0])  # Number of features in the input data
        self.weights = [random.uniform(-0.1, 0.1) for _ in range(num_features)]
        self.bias = random.uniform(-0.1, 0.1)

        for epoch in range(epochs):
            weight_gradients = [0] * num_features
            bias_gradient = 0
            total_loss = 0

            for features, target in data:
                # Prediction: y = w1*x1 + w2*x2 + ... + wn*xn + b
                prediction = sum(w * x for w, x in zip(self.weights, features)) + self.bias
                error = prediction - target
                total_loss += error ** 2  # Mean Squared Error

                # Gradients calculation
                for i in range(num_features):
                    weight_gradients[i] += error * features[i]
                bias_gradient += error

            # Update weights and bias
            for i in range(num_features):
                self.weights[i] -= learning_rate * weight_gradients[i] / len(data)
            self.bias -= learning_rate * bias_gradient / len(data)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss / len(data)}")

    def predict(self, features):
        """
        Predicts the target value for a given set of features.
        :param features: List of numerical values.
        :return: Predicted value.
        """
        return sum(w * x for w, x in zip(self.weights, features)) + self.bias