-- Table to store training data for Linear Regression
CREATE TABLE response_length_training_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_words INTEGER NOT NULL,
    avg_word_length REAL NOT NULL,
    response_length INTEGER NOT NULL
);

-- Table to store sentence classification data
CREATE TABLE sentence_classification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sentence TEXT NOT NULL,
    classification TEXT NOT NULL
);

-- Table to store trained Linear Regression model parameters
CREATE TABLE linear_regression_model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feature_weights TEXT NOT NULL, -- Serialized list of weights
    bias REAL NOT NULL
);

-- Table to store predicted response data for debugging/analytics
CREATE TABLE predicted_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_sentence TEXT NOT NULL,
    predicted_length INTEGER NOT NULL,
    actual_response TEXT NOT NULL
);