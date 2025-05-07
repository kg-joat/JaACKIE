from data_manager import DataManager
from predictive_model import PredictiveModel

# Initialize DataManager and PredictiveModel
data_manager = DataManager("chatbot.db")
data_manager.create_tables()
predictive_model = PredictiveModel("chatbot.db")

# Example training data
training_data = [
    (5, 4.2, 10),  # (num_words, avg_word_length, response_length)
    (10, 4.0, 20),
    (7, 3.8, 15),
]

# Log training data into response_length_training_data
for num_words, avg_word_length, response_length in training_data:
    data_manager.log_training_data(num_words, avg_word_length, response_length)

# Example sentence classification data
classification_data = [
    ("Hello, how are you?", "Greeting"),
    ("What is the weather like?", "Question"),
    ("Tell me a joke.", "Command"),
]

# Log sentence classification data into sentence_classification
for sentence, classification in classification_data:
    data_manager.log_sentence_classification(sentence, classification)