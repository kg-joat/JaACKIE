from flask import Flask, request, jsonify
from predictive_model import PredictiveModel

# Initialize Flask app
app = Flask(__name__)

# Initialize the predictive model
predictive_model = PredictiveModel("chatbot.db")

@app.route('/respond', methods=['POST'])
def respond():
    """
    Endpoint to handle user input and generate a bot response.
    """
    try:
        # Parse incoming JSON data
        data = request.get_json()
        user_input = data.get('user_input', '')

        # Generate a response using the predictive model
        bot_response = predictive_model.generate_response(user_input)

        # Return the response as JSON
        return jsonify(bot_response)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "An error occurred.", "mode": "chatting"}), 500

if __name__ == '__main__':
    app.run(debug=True)