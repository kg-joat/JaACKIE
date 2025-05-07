from machine_learning import LinearRegression
from data_manager import DataManager


class PredictiveModel:
    def __init__(self, db_name):
        self.data_manager = DataManager(db_name)
        self.data_manager.create_tables()
        self.response_length_predictor = LinearRegression()

        # Load existing model parameters if available
        weights, bias = self.data_manager.load_linear_model()
        if weights and bias:
            self.response_length_predictor.weights = weights
            self.response_length_predictor.bias = bias

    def train_response_length_model(self, training_data):
        """
        Train the Linear Regression model to predict response lengths.
        :param training_data: List of tuples [(features, response_length)],
                              where features are numerical attributes of the input.
        """
        self.response_length_predictor.train(training_data, learning_rate=0.01, epochs=1000)

        # Save the trained model parameters
        self.data_manager.save_linear_model(
            self.response_length_predictor.weights,
            self.response_length_predictor.bias
        )

    def generate_response(self, user_input):
        """
        Generates a response based on user input and predicted response length.
        """
        # Example features for prediction: [number_of_words, average_word_length]
        words = user_input.split()
        num_words = len(words)
        avg_word_length = sum(len(word) for word in words) / num_words if num_words > 0 else 0
        features = [num_words, avg_word_length]

        # Predict response length
        predicted_length = int(self.response_length_predictor.predict(features))

        # Log the prediction
        response = " ".join(["response_word"] * predicted_length)  # Placeholder response
        self.data_manager.log_predicted_response(user_input, predicted_length, response)
        return response