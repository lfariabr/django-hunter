import os
import json
import pandas as pd
import numpy as np
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample recommendation logic
# def prepare_data_and_similarity():
#     # Load or prepare data
#     df = pd.DataFrame()
#     cosine_sim = cosine_similarity(df)
#     indices = pd.Series(df.index, index=df['procedure_name'])
#     return df, cosine_sim, indices
# Updated recommendation logic with the full path to your JSON file

def apply_tfidf(df):
    complaint_texts = df['complaint_vector'].apply(lambda x: ' '.join(x))
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(complaint_texts)
    return tfidf_matrix

# Then we could trigger it by: tfidf_matrix = apply_tfidf(df)

def prepare_data_and_similarity():
    # Specify the full path to procedures.json
    json_file_path = os.path.join(settings.BASE_DIR, 'procedures', 'procedures.json')

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found at: {json_file_path}")
    
    # Load the JSON data into a DataFrame
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    if 'id' not in df.columns:
        df['id'] = df.index
    
    if df.empty:
        raise ValueError("The DataFrame is empty. Cannot proceed with the recommendation algorithm.")
    
    # Normalize 'cost' for comparison
    df['custo_normalizado'] = (df['cost'] - df['cost'].min()) / (df['cost'].max() - df['cost'].min())

    # Tokenize 'complaint' (assuming complaints are comma-separated)
    df['complaint_vector'] = df['complaint'].apply(lambda x: x.split(', '))

    # Calculate cosine similarity (for now based on normalized cost)
    # Meaning that procedures with similar costs will have similar similarity scores
    cosine_sim = cosine_similarity(df[['custo_normalizado']])

    # Create indices based on procedure names
    indices = pd.Series(df.index, index=df['name']).drop_duplicates()

    return df, cosine_sim, indices

# We're using similarity = 0, custo = 0.5, queixa = 0.5 
# which seems more appropriate for initial testing phase
def get_recommendations_multi(procedures, cosine_sim, df, indices, peso_similaridade=0.0, peso_custo=0.5, peso_queixa=0.5):
    
    # Finding indices of input procedures in the DataFrame
    idx_list = [indices[proc] for proc in procedures]

    # Collecting complaints for input procedures
    input_complaints = set()
    for idx in idx_list:
        procedure_complaints = df.loc[idx, 'complaint_vector']
        input_complaints.update(procedure_complaints)

    # Calculating the similarity scores
    sim_scores = [list(enumerate(cosine_sim[idx])) for idx in idx_list]
    avg_sim_scores = np.mean([np.array([score[1] for score in scores]) for scores in sim_scores], axis=0)

    # Creating DataFrame for similarity scores
    sim_scores_df = pd.DataFrame(list(enumerate(avg_sim_scores)), columns=['index', 'similarity_score'])
    
    # Add normalized cost
    sim_scores_df['custo_normalizado'] = df.loc[sim_scores_df['index'], 'custo_normalizado'].values

    # Calculating the complaint similarity using Jaccard similarity
    complaint_scores = []
    for idx in sim_scores_df['index']:
        candidate_complaints = df.loc[idx, 'complaint_vector']

        # This counts how many complaints are shared between input procedures and candidate procedures
        overlap = len(set(candidate_complaints) & input_complaints)

        # Union counts total number of unique complaints across input and candidate procedures
        total_complaints = len(set(candidate_complaints) | input_complaints)

        if total_complaints > 0:
            complaint_score = overlap / total_complaints
        else:
            complaint_score = 0
        complaint_scores.append(complaint_score)
    
    sim_scores_df['queixa_score'] = complaint_scores

    # Calculate final score
    sim_scores_df['score'] = (
        peso_similaridade * sim_scores_df['similarity_score'] +
        peso_custo * sim_scores_df['custo_normalizado'] +
        peso_queixa * sim_scores_df['queixa_score']
    )

    # Remove input procedures from recommendations
    sim_scores_df = sim_scores_df[~sim_scores_df['index'].isin(idx_list)]

    # Sort by highest scores and select top 5
    sim_scores_df = sim_scores_df.sort_values(by='score', ascending=False)
    top_indices = sim_scores_df.head(5)['index'].values

    recommended_df = df.iloc[top_indices].copy()
    recommended_df['score'] = sim_scores_df.head(5)['score'].values # Including score in the response

    # Return recommended procedures
    # return df.iloc[top_indices]
    return recommended_df