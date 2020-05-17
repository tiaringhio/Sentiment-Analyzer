import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
import string
from statistics import mode
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Loading model with pickle
LRClassifier = ".\\Resources\\LRClassifier.pkl"
with open(LRClassifier, 'rb') as file:
    LRClassifier = pickle.load(file)


# Italian stopwords
stop_words = stopwords.words('italian')

# Italian Stemmer
stemmer = SnowballStemmer('italian')


# Additional stopwords found online
def additional_stop_words():
    with open('..\\Training\\stopwords.txt', 'r') as f:
        additional_stopwords = f.readlines()
    additional_stopwords = [x.strip() for x in additional_stopwords]
    return additional_stopwords


# Function to remove noise from tokens, removing also stopwords
def remove_noise(tweet_tokens, stop_words=(), additional_stop_words=()):
    cleaned_tokens = []
    for token in tweet_tokens:
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)
        token = stemmer.stem(token)
        if len(token) > 3 and token not in string.punctuation and token.lower() not in stop_words and token.lower() not in additional_stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def sentiment(tweet):
    predictions = []
    custom_tokens = remove_noise(word_tokenize(tweet))
    confidence_p = LRClassifier.prob_classify(
        dict([token, True] for token in custom_tokens)).prob('Positive')
    confidence_n = LRClassifier.prob_classify(
        dict([token, True] for token in custom_tokens)).prob('Negative')
    polarity = confidence_p - confidence_n

    sentiment = ''
    if polarity > 0:
        sentiment = 'positivo'
    else:
        sentiment = 'negativo'

    predictions.append(sentiment)
    predictions.append(polarity)
    return predictions


def getSentiment(predictions):
    sent = predictions[0]
    return sent


def getPolarity(predictions):
    pol = predictions[1]
    return pol


def getConfidence(predictions):
    pol = predictions[1]
    confidence = ''
    # Super confident
    if(pol > 0.75 or pol < -0.75):
        confidence = 'Ne sono piuttosto sicuro! 😎\n'
    # Very confident
    elif pol > 0.5 and pol <= 0.75 or pol < -0.5 and pol >= -0.75:
        confidence = 'Ne sono piuttosto sicuro! 😉\n'
    # Confident enough
    elif pol > 0.25 and pol <= 0.5 or pol < -0.25 and pol >= -0.5:
        confidence = 'Ne sono abbastanza sicuro! 🤗\n'
    # Not really confident
    elif pol > 0 and pol <= 0.25 or pol < 0 and pol >= -0.25:
        confidence = 'Non ne sono così sicuro però 🤔\n'
    return confidence
