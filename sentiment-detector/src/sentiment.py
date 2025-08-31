import re

class SentimentAnalyzer:
    def __init__(self):
        # Simple lists of positive and negative words for demonstration
        self.positive_words = {"good", "great", "excellent", "happy", "love", "wonderful", "amazing", "awesome", "fantastic", "positive"}
        self.negative_words = {"bad", "terrible", "awful", "sad", "hate", "horrible", "worst", "negative", "poor", "disappointing"}

    def analyze_sentiment(self, text, mode="Simple"):
        text = text.lower()
        words = set(re.findall(r'\b\w+\b', text))

        if mode == "Simple":
            # Simple: positive if more positive words, negative if more negative, else neutral
            pos_count = len(words & self.positive_words)
            neg_count = len(words & self.negative_words)
            if pos_count > neg_count:
                return "Positive", round(pos_count / (pos_count + neg_count + 1), 2)
            elif neg_count > pos_count:
                return "Negative", round(neg_count / (pos_count + neg_count + 1), 2)
            else:
                return "Neutral", 0.5
        elif mode == "Advanced":
            # Advanced: crude scoring based on word frequency
            pos_count = sum(1 for w in re.findall(r'\b\w+\b', text) if w in self.positive_words)
            neg_count = sum(1 for w in re.findall(r'\b\w+\b', text) if w in self.negative_words)
            total = pos_count + neg_count
            if total == 0:
                return "Neutral", 0.5
            score = pos_count / total
            if score > 0.6:
                return "Positive", round(score, 2)
            elif score < 0.4:
                return "Negative", round(1 - score, 2)
            else:
                return "Neutral", round(score, 2)
        else:
            return "Neutral", 0.5