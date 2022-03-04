import pandas as pd
import numpy as np 
import sklearn
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from util import text_preprocessing

# path of text dataset
data_path = './dataset/COMP3074-CW1-Dataset-QA.csv'

def answer_Q(query, threshold):

    df = pd.read_csv(data_path)
    df['processed_Q'] = df['Question'].apply(text_preprocessing, type = 'stemming')
    # df['processed_A'] = df['Answer'].apply(text_preprocessing, type = 'stemming')

    # TF-IDF
    tfidf_vec = TfidfVectorizer(analyzer='word')
    X_tfidf = tfidf_vec.fit_transform(df['Question']).toarray()
    df_tfidf = pd.DataFrame(X_tfidf, columns = tfidf_vec.get_feature_names())

    # process query and find the answer
    processed_query = text_preprocessing(query, 'stemming')
    input_tfidf = tfidf_vec.transform([processed_query]).toarray()
    cos = 1 - pairwise_distances(df_tfidf, input_tfidf, metric = 'cosine')
    
    if cos.max() >= threshold:
        id_argmax = np.where(cos == np.max(cos, axis=0))
        id = np.random.choice(id_argmax[0]) 
        return df['Answer'].loc[id]
    else:
        return 'NOT FOUND'

