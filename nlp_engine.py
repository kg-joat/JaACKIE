import re

class NLPEngine:
    def __init__(self):
        pass

    def tokenize(self, text):
        """
        Tokenizes the text into words and punctuation.
        """
        return re.findall(r"\w+|[.,!?;]", text)

    def classify_sentence(self, sentence):
        """
        Classifies the sentence type as Declarative, Interrogative,
        Imperative, or Exclamatory.
        """
        sentence = sentence.strip()
        if sentence.endswith('?'):
            return "Interrogative"
        elif sentence.endswith('!'):
            return "Exclamatory"
        elif sentence.lower().startswith(("please", "kindly", "do", "could", "would")) or sentence.split()[0].lower() in {"open", "close", "stop", "start"}:
            return "Imperative"
        else:
            return "Declarative"

    def analyze_sentence(self, sentence):
        """
        Tokenizes and classifies a sentence.
        """
        tokens = self.tokenize(sentence)
        sentence_type = self.classify_sentence(sentence)
        return {
            "tokens": tokens,
            "type": sentence_type
        }