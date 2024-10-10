from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')
import numpy as np
import pandas as pd
from ..models import Procedure

def get_recommendations_multi(
    procedimentos, 
    cosine_sim, 
    df, 
    indices, 
    peso_similaridade=0.0, 
    peso_custo=0.5, 
    peso_queixa=0.5
):
    # Get the indices of the input procedures
    idx_list = [indices.get(proc) for proc in procedimentos]

    # Collect 'Queixas' from the input procedures
    input_queixas = set()
    for idx in idx_list:
        proc_queixas = df.loc[idx, 'complaint']
        input_queixas.update(proc_queixas)

    # Calculate average similarity scores
    sim_scores = [list(enumerate(cosine_sim[idx])) for idx in idx_list]
    avg_sim_scores = np.mean([np.array([score[1] for score in scores]) for scores in sim_scores], axis=0)

    # Create a DataFrame with the similarity scores
    sim_scores_df = pd.DataFrame(list(enumerate(avg_sim_scores)), columns=['index', 'similarity_score'])

    # Add normalized cost to the DataFrame
    sim_scores_df['custo_normalizado'] = df.loc[sim_scores_df['index'], 'custo_normalizado'].values

    # Calculate complaint similarity scores
    queixa_scores = []
    for idx in sim_scores_df['index']:
        candidate_queixas = df.loc[idx, 'complaint']
        overlap = len(set(candidate_queixas) & input_queixas)
        total_queixas = len(set(candidate_queixas) | input_queixas)
        queixa_score = overlap / total_queixas if total_queixas > 0 else 0
        queixa_scores.append(queixa_score)

    sim_scores_df['queixa_score'] = queixa_scores

    # Calculate the combined score
    sim_scores_df['score'] = (
        peso_similaridade * sim_scores_df['similarity_score'] +
        peso_custo * sim_scores_df['custo_normalizado'] +
        peso_queixa * sim_scores_df['queixa_score']
    )

    # Exclude the input procedures from recommendations
    sim_scores_df = sim_scores_df[~sim_scores_df['index'].isin(idx_list)]

    # Sort by the combined score and get the top 5 recommendations
    sim_scores_df = sim_scores_df.sort_values(by='score', ascending=False)
    top_indices = sim_scores_df.head(5)['index'].values

    # Retrieve the recommended procedures from the DataFrame
    recommended_procedures = df.iloc[top_indices].copy()
    recommended_procedures['score'] = sim_scores_df.head(5)['score'].values

    return recommended_procedures

def prepare_data_and_similarity():
    # Query all procedures
    procedures = Procedure.objects.all()
    
    # Create a DataFrame from procedures
    df = pd.DataFrame(list(procedures.values('id', 'name', 'description', 'cost', 'complaint')))
    
    # Normalize cost (e.g., scale to 0-1)
    df['custo_normalizado'] = (df['cost'] - df['cost'].min()) / (df['cost'].max() - df['cost'].min())

    # Combine text fields for TF-IDF (e.g., description + complaints)
    df['combined_text'] = df['description'] + ' ' + df['complaint']

    # Create the TF-IDF matrix based on the combined text
    # tfidf_vectorizer = TfidfVectorizer()
    from nltk.corpus import stopwords
    portuguese_stop_words = stopwords.words('portuguese')
    tfidf_vectorizer = TfidfVectorizer(stop_words=portuguese_stop_words)

    # Create the TF-IDF matrix
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_text'])

    # Calculate the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Create an index mapping for fast look-up
    indices = pd.Series(df.index, index=df['name']).to_dict()

    return df, cosine_sim, indices