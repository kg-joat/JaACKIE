import sqlite3
import json


class DataManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """
        Creates required tables if they do not exist.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS response_length_training_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_words INTEGER NOT NULL,
            avg_word_length REAL NOT NULL,
            response_length INTEGER NOT NULL
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentence_classification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence TEXT NOT NULL,
            classification TEXT NOT NULL
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS linear_regression_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_weights TEXT NOT NULL,
            bias REAL NOT NULL
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS predicted_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_sentence TEXT NOT NULL,
            predicted_length INTEGER NOT NULL,
            actual_response TEXT NOT NULL
        )""")
        self.connection.commit()

    def log_training_data(self, num_words, avg_word_length, response_length):
        """
        Logs training data for Linear Regression.
        """
        self.cursor.execute("""
        INSERT INTO response_length_training_data (num_words, avg_word_length, response_length)
        VALUES (?, ?, ?)""", (num_words, avg_word_length, response_length))
        self.connection.commit()

    def save_linear_model(self, weights, bias):
        """
        Saves Linear Regression model parameters.
        """
        self.cursor.execute("""
        INSERT INTO linear_regression_model (feature_weights, bias)
        VALUES (?, ?)""", (json.dumps(weights), bias))
        self.connection.commit()

    def load_linear_model(self):
        """
        Loads the most recent Linear Regression model parameters.
        """
        self.cursor.execute("""
        SELECT feature_weights, bias FROM linear_regression_model
        ORDER BY id DESC LIMIT 1""")
        row = self.cursor.fetchone()
        if row:
            weights = json.loads(row[0])
            bias = row[1]
            return weights, bias
        return None, None

    def log_predicted_response(self, input_sentence, predicted_length, actual_response):
        """
        Logs predicted responses for debugging/analytics.
        """
        self.cursor.execute("""
        INSERT INTO predicted_responses (input_sentence, predicted_length, actual_response)
        VALUES (?, ?, ?)""", (input_sentence, predicted_length, actual_response))
        self.connection.commit()