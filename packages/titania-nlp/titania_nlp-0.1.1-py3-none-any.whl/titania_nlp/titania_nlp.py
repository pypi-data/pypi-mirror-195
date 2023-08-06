import spacy
from spacy.lang.en import English
from spacytextblob.spacytextblob import SpacyTextBlob

class NLPModel:
    def __init__(self):
        self.nlp = English()
        self.nlp.add_pipe(SpacyTextBlob())

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def get_sentiment(self, text):
        doc = self.nlp(text)
        sentiment = doc._.polarity
        sentiment = round(sentiment, 2)
        if sentiment > 0:
            spacy_sentiment = "POSITIVE"
        else:
            spacy_sentiment = "NEGATIVE"
        positive_words = []
        negative_words = []
        for x in doc._.assessments:
            if x[1] > 0:
                positive_words.append(x[0][0])
            elif x[1] < 0:
                negative_words.append(x[0][0])
        spacy_positive_words = str(positive_words)
        spacy_negative_words = str(negative_words)
        return spacy_sentiment, sentiment, spacy_positive_words, spacy_negative_words