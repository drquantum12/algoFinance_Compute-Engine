from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Sentiment:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text):
        return self.analyzer.polarity_scores(text)
    
    def get_sentiment(self, text):
        sentiment = self.analyze(text)
        if sentiment["compound"] >= 0.05:
            return "Positive"
        elif sentiment["compound"] <= -0.05:
            return "Negative"
        else:
            return "Neutral"