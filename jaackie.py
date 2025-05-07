from machine_learning import LinearRegression

class Chatbot:
    def __init__(self):
        # Initialize the Linear Regression model
        self.response_length_predictor = LinearRegression()

    def train_response_length_model(self, training_data):
        """
        Train the Linear Regression model to predict response lengths.
        :param training_data: List of tuples [(features, response_length)], where features are numerical attributes of the input.
        """
        self.response_length_predictor.train(training_data, learning_rate=0.01, epochs=1000)

    def generate_response(self, user_input):
        """
        Generates a response based on user input and predicted response length.
        """
        # Example features for prediction: [number_of_words, average_word_length]
        features = [len(user_input.split()), sum(len(word) for word in user_input.split()) / len(user_input.split())]
        predicted_length = int(self.response_length_predictor.predict(features))

        # Generate a response of approximately the predicted length
        response = " ".join(["response_word"] * predicted_length)
        return response