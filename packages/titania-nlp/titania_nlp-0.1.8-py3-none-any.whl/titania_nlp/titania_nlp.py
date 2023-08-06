import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities


def get_sentiment(text, nlp):
    text_blob = SpacyTextBlob(nlp=nlp)
    doc = nlp(text)
    sentiment = text_blob(doc).polarity
    sentiment = round(sentiment, 2)
    if sentiment > 0:
        spacy_sentiment = "POSITIVE"
    else:
        spacy_sentiment = "NEGATIVE"
    positive_words = []
    negative_words = []
    for x in text_blob(doc).assessments:
        if x[1] > 0:
            positive_words.append(x[0])
        elif x[1] < 0:
            negative_words.append(x[0])
        else:
            pass
    spacy_positive_words = str(positive_words)
    spacy_negative_words = str(negative_words)
    return spacy_sentiment, sentiment, spacy_positive_words, spacy_negative_words
