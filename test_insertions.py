from data_manager import DataManager

# Initialize DataManager
data_manager = DataManager("chatbot.db")

# Create tables if they don't exist
data_manager.create_tables()

# Test logging training data
data_manager.log_training_data(5, 4.2, 10)

# Test logging sentence classification data
data_manager.log_sentence_classification("Hello, how are you?", "Greeting")