import pandas as pd
import numpy as np 
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from util import text_preprocessing

# path of small talk dataset
data_path = './dataset/COMP3074-CW1-Dataset-small_talk.csv'

def talk_response(query, threshold):

    df = pd.read_csv(data_path)

    # TF-IDF
    tfidf_vec = TfidfVectorizer(analyzer='word')
    X_tfidf = tfidf_vec.fit_transform(df['Question']).toarray()
    df_tfidf = pd.DataFrame(X_tfidf, columns = tfidf_vec.get_feature_names())

    # process query 
    input_tfidf = tfidf_vec.transform([query.lower()]).toarray()

    # cosine similarity
    cos = 1 - pairwise_distances(df_tfidf, input_tfidf, metric = 'cosine')
    
    if cos.max() >= threshold:
        id_argmax = np.where(cos == np.max(cos, axis=0))
        id = np.random.choice(id_argmax[0]) 
        return df['Answer'].loc[id]
    else:
        return 'NOT FOUND'
    
if __name__ == "__main__":
    print(talk_response("What is up", 0.1))

