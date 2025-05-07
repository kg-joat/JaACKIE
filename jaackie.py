from machine_learning import LinearRegression
from predictive_model import PredictiveModel  # Fixed import error
from gui import ChatbotGUI
from nlp_engine import NLPEngine

# Entry point for the JaACKIE chatbot
def main():
    print("Initializing JaACKIE chatbot...")
    try:
        # Initialize components
        nlp_engine = NLPEngine()
        predictive_model = PredictiveModel(db_name="chatbot.db")

        # Insert sample responses and train the model
        predictive_model.data_manager.create_tables()
        predictive_model.data_manager.insert_sample_responses()
        training_data = [
            ([2, 3.5], 3),  # Example: [number_of_words, avg_word_length], response_length
            ([3, 4.0], 4),
            ([4, 5.0], 5),
        ]
        predictive_model.train_response_length_model(training_data)

        # Define callbacks for GUI interaction
        def send_callback(user_input):
            try:
                # Step 1: Analyze user input
                analysis = nlp_engine.analyze_sentence(user_input)
                print(f"User Input Analysis: {analysis}")

                # Step 2: Generate response using predictive model
                response = predictive_model.generate_response(user_input)
                if not response:
                    print("Error: Predictive model returned an empty response.")
                    return "Sorry, I couldn't generate a response."

                print(f"Generated Response: {response}")
                return response
            except Exception as e:
                print(f"Error in send_callback: {e}")
                return "An error occurred while processing your input."

        def observation_mode_callback(enabled):
            print(f"Observation mode {'enabled' if enabled else 'disabled'}.")

        def feedback_callback(feedback_type, user_input, bot_response):
            print(f"Feedback received: {feedback_type} for input '{user_input}' and response '{bot_response}'")
            return None

        # Initialize the GUI and start the chatbot application
        print("Launching GUI...")
        gui = ChatbotGUI(send_callback, observation_mode_callback, feedback_callback)
        gui.run()
    except Exception as e:
        print(f"Error initializing JaACKIE chatbot: {e}")

if __name__ == "__main__":
    print("Starting JaACKIE.py...")
    main()