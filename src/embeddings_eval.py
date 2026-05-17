import pandas as pd

def get_nearest_neighbors(model, word, topn=5):
    """
    Повертає список найближчих сусідів для слова з конкретної моделі.
    Обробляє ситуацію, коли слова немає в словнику (OOV).
    """
    try:
        # Для Word2Vec слово має бути в словнику. 
        # FastText може згенерувати вектор для OOV слова.
        neighbors = model.wv.most_similar(word, topn=topn)
        return [f"{w} ({score:.3f})" for w, score in neighbors]
    except KeyError:
        return ["OOV (Out of Vocabulary)"]

def compare_models_neighbors(w2v_model, ft_model, words_list, topn=5):
    """
    Створює pandas DataFrame для зручного порівняння сусідів 
    між Word2Vec та FastText для списку слів.
    """
    results = []
    
    for word in words_list:
        w2v_neighbors = get_nearest_neighbors(w2v_model, word, topn)
        ft_neighbors = get_nearest_neighbors(ft_model, word, topn)
        
        results.append({
            'Word': word,
            'Word2Vec Neighbors': ", ".join(w2v_neighbors),
            'FastText Neighbors': ", ".join(ft_neighbors)
        })
        
    return pd.DataFrame(results)