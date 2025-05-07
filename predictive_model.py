from machine_learning import LinearRegression
from data_manager import DataManager
import random


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
        for features, response_length in training_data:
            num_words, avg_word_length = features
            # Log to the database
            self.data_manager.log_training_data(num_words, avg_word_length, response_length)

        # Train the model
        self.response_length_predictor.train(training_data, learning_rate=0.01, epochs=1000)

        # Save the trained model parameters
        self.data_manager.save_linear_model(
            self.response_length_predictor.weights,
            self.response_length_predictor.bias
        )

    def generate_response(self, user_input):
        """
        Generates a response based on user input and predicted response length.
        Returns a mode to determine whether the bot is in learning or chatting mode.
        """
        try:
            # Respond by repeating the user's statement in learning mode
            print("Gathering information... (Learning Mode)")
            return {
                "response": user_input,  # Repeat the user's input
                "mode": "learning"  # Indicate learning mode to the frontend
            }
        except Exception as e:
            print(f"Error predicting response: {e}")
            print("Falling back to past responses.")
            return {
                "response": self.get_past_response(user_input),
                "mode": "chatting"  # Default to normal chatting mode
            }

    def get_past_response(self, user_input):
        """
        Retrieves a relevant past response based on similarity to the user input.
        If no relevant responses are found, returns a random response.
        """
        try:
            # Fetch all past responses
            self.data_manager.cursor.execute("""
                SELECT input_sentence, actual_response
                FROM predicted_responses
            """)
            rows = self.data_manager.cursor.fetchall()

            if not rows:
                print("Predicted responses table is empty.")
                return "I'm sorry, I don't have enough data to guess a response."

            # Find the most similar past response (basic similarity based on word overlap)
            best_match = None
            max_overlap = 0

            input_words = set(user_input.split())
            for input_sentence, actual_response in rows:
                response_words = set(input_sentence.split())
                overlap = len(input_words & response_words)  # Intersection of words
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_match = actual_response

            return best_match if best_match else random.choice([row[1] for row in rows])

        except Exception as e:
            print(f"Error retrieving past response: {e}")
            return "I'm sorry, I don't have an answer for that right now."