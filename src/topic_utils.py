import numpy as np

def get_top_words(pipeline, n_words=10):
    """
    Повертає словник, де ключ - номер теми, а значення - список топ-N слів.
    Підтримує як LSA, так і LDA пайплайни.
    """
    # Визначаємо, який саме алгоритм у пайплайні
    if 'svd' in pipeline.named_steps:
        model = pipeline.named_steps['svd']
        vectorizer = pipeline.named_steps['tfidf']
    elif 'lda' in pipeline.named_steps:
        model = pipeline.named_steps['lda']
        vectorizer = pipeline.named_steps['count']
    else:
        raise ValueError("Pipeline must contain 'svd' or 'lda' step.")

    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    
    for topic_idx, topic_weights in enumerate(model.components_):
        # Сортуємо індекси ваг за спаданням і беремо перші n_words
        top_features_ind = topic_weights.argsort()[:-n_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        topics[topic_idx] = top_features
        
    return topics

def get_top_documents(pipeline, texts, n_docs=3):
    """
    Повертає топ-N документів для кожної теми на основі їхньої ваги/ймовірності.
    """
    # Отримуємо матрицю розподілу тем для всіх документів
    topic_distributions = pipeline.transform(texts)
    
    topics_docs = {}
    n_topics = topic_distributions.shape[1]
    
    # Конвертуємо Pandas Series в список для безпечного доступу за індексом
    texts_list = texts.tolist() if hasattr(texts, 'tolist') else list(texts)
    
    for topic_idx in range(n_topics):
        # Знаходимо індекси документів з найбільшим скором для поточної теми
        top_doc_indices = np.argsort(topic_distributions[:, topic_idx])[::-1][:n_docs]
        
        docs = []
        for doc_idx in top_doc_indices:
            score = topic_distributions[doc_idx, topic_idx]
            docs.append((texts_list[doc_idx], score))
            
        topics_docs[topic_idx] = docs
        
    return topics_docs