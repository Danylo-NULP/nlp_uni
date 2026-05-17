from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
from sklearn.pipeline import Pipeline

def build_lsa_pipeline(n_topics=5, ngram_range=(1, 1), min_df=3, max_df=0.9, max_features=5000):
    """
    Створює Pipeline для LSA (Latent Semantic Analysis).
    Використовує TF-IDF + TruncatedSVD.
    """
    vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        max_features=max_features,
        stop_words='english'
    )
    
    svd = TruncatedSVD(n_components=n_topics, random_state=42)
    
    return Pipeline([
        ('tfidf', vectorizer),
        ('svd', svd)
    ])

def build_lda_pipeline(n_topics=5, ngram_range=(1, 1), min_df=3, max_df=0.9, max_features=5000):
    """
    Створює Pipeline для LDA (Latent Dirichlet Allocation).
    Використовує CountVectorizer + LDA.
    """
    vectorizer = CountVectorizer(
        analyzer='word',
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        max_features=max_features,
        stop_words='english'
    )
    
    lda = LatentDirichletAllocation(
        n_components=n_topics, 
        random_state=42, 
        n_jobs=-1
    )
    
    return Pipeline([
        ('count', vectorizer),
        ('lda', lda)
    ])