import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import boto3
import json

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
    tb_doc = text_blob(doc)
    sentiment = tb_doc._.polarity
    sentiment = round(sentiment, 2)
    if sentiment > 0:
        spacy_sentiment = "POSITIVE"
    else:
        spacy_sentiment = "NEGATIVE"
    positive_words = []
    negative_words = []
    for x in tb_doc._.assessments:
        if x[1] > 0:
            positive_words.append(x[0])
        elif x[1] < 0:
            negative_words.append(x[0])
        else:
            pass
    spacy_positive_words = str(positive_words)
    spacy_negative_words = str(negative_words)
    return spacy_sentiment, sentiment, spacy_positive_words, spacy_negative_words

def get_nltk_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    sentiment = ''
    if scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return sentiment, scores['neg'], scores['neu'], scores['pos'], scores['compound']


s3 = boto3.resource('s3',
         aws_access_key_id="AKIATKSEH532EWWG4BM7",
         aws_secret_access_key= "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")

comprehend = boto3.client(service_name='comprehend', region_name='ap-south-1',aws_access_key_id="AKIATKSEH532EWWG4BM7",
         aws_secret_access_key= "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")

def get_amazon_sentiment_scores(text):
    try:
        entities = comprehend.detect_entities(Text=text, LanguageCode='en')
        textEntities = [dict_item['Text'] for dict_item in entities['Entities']]
        typeEntities = [dict_item['Type'] for dict_item in entities['Entities']]
        sentiment_scores = comprehend.detect_sentiment(Text=text, LanguageCode='en')['SentimentScore']
        return sentiment_scores
    except:
        print("Exception")
