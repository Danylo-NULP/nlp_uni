from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline, FeatureUnion

def create_svm_pipeline(feature_mode='word', word_ngram=(1,2), char_ngram=(3,5), class_weight=None, max_features=5000):
    """
    Створює Pipeline з LinearSVC. 
    Підтримує три режими ознак: 'word', 'char', 'word_char'.
    """
    if feature_mode == 'word':
        vectorizer = TfidfVectorizer(
            analyzer='word', 
            ngram_range=word_ngram, 
            sublinear_tf=True, 
            max_features=max_features
        )
    elif feature_mode == 'char':
        # Для символів рекомендується char_wb (word boundaries), щоб не брати пробіли між словами
        vectorizer = TfidfVectorizer(
            analyzer='char_wb', 
            ngram_range=char_ngram, 
            sublinear_tf=True, 
            max_features=max_features
        )
    elif feature_mode == 'word_char':
        # Комбінуємо ознаки: половина фіч для слів, половина для символів
        word_vec = TfidfVectorizer(analyzer='word', ngram_range=word_ngram, sublinear_tf=True, max_features=max_features//2)
        char_vec = TfidfVectorizer(analyzer='char_wb', ngram_range=char_ngram, sublinear_tf=True, max_features=max_features//2)
        
        vectorizer = FeatureUnion([
            ('word', word_vec),
            ('char', char_vec)
        ])
    else:
        raise ValueError("Invalid feature_mode. Use 'word', 'char', or 'word_char'.")

    # dual=False рекомендується для випадків, коли кількість зразків більша за кількість фіч
    classifier = LinearSVC(C=1.0, class_weight=class_weight, random_state=42, dual=False)

    return Pipeline([
        ('features', vectorizer),
        ('clf', classifier)
    ])