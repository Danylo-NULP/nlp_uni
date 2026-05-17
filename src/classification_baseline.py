import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

def create_baseline_pipeline(ngram_range=(1, 1), max_features=5000, class_weight=None, max_iter=300):
    """
    Створює scikit-learn Pipeline для класифікації тексту.
    Гарантує, що векторизатор навчається (fit) ТІЛЬКИ на тренувальній вибірці.
    """
    vectorizer = TfidfVectorizer(
        analyzer="word", 
        ngram_range=ngram_range, 
        sublinear_tf=True, 
        max_features=max_features
    )
    
    classifier = LogisticRegression(
        max_iter=max_iter, 
        class_weight=class_weight, 
        random_state=42
    )
    
    return Pipeline([
        ('tfidf', vectorizer),
        ('clf', classifier)
    ])

def evaluate_pipeline(pipeline, X_train, y_train, X_eval, y_eval):
    """
    Навчає Pipeline на тренувальних даних та оцінює на тестових/валідаційних.
    Повертає словник з усіма необхідними метриками.
    """
    # FIT виключно на X_train
    pipeline.fit(X_train, y_train)
    
    # TRANSFORM неявно викликається всередині predict для X_eval
    y_pred = pipeline.predict(X_eval)

    acc = accuracy_score(y_eval, y_pred)
    f1_macro = f1_score(y_eval, y_pred, average='macro')
    report_dict = classification_report(y_eval, y_pred, output_dict=True)
    report_str = classification_report(y_eval, y_pred)
    cm = confusion_matrix(y_eval, y_pred)
    classes = pipeline.classes_

    return {
        'accuracy': acc,
        'f1_macro': f1_macro,
        'report_dict': report_dict,
        'report_str': report_str,
        'confusion_matrix': cm,
        'classes': classes,
        'y_pred': y_pred
    }

def extract_top_features(pipeline, top_n=10):
    """
    Витягує топ-N найважливіших фіч (слів/біграм) для кожного класу
    на основі ваг логістичної регресії.
    """
    vectorizer = pipeline.named_steps['tfidf']
    classifier = pipeline.named_steps['clf']
    
    feature_names = vectorizer.get_feature_names_out()
    classes = classifier.classes_
    top_features = {}

    # Для багатокласової класифікації (як у нашому SNLI: 3 класи)
    for i, class_label in enumerate(classes):
        coefs = classifier.coef_[i]
        # Беремо індекси топ-N найбільших ваг
        top_indices = np.argsort(coefs)[-top_n:][::-1]
        top_features[class_label] = [(feature_names[j], coefs[j]) for j in top_indices]

    return top_features