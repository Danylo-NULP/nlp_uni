import spacy

# Завантажуємо spaCy, вимикаючи зайві компоненти для швидкості
try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "textcat"])
except OSError:
    import warnings
    warnings.warn("Модель 'en_core_web_sm' не знайдена. Виконайте: python -m spacy download en_core_web_sm")
    nlp = None

def extract_ling_features(text: str) -> dict:
    """
    Повертає лематизований текст та послідовність POS-тегів.
    """
    if not isinstance(text, str) or not text.strip() or not nlp:
        return {"lemma_text": "", "pos_seq": "", "pos_text": ""}
    
    doc = nlp(text)
    lemmas = []
    pos_tags = []
    pos_text_pairs = []
    
    for token in doc:
        # Беремо лему в нижньому регістрі (це стандарт для ML)
        lemmas.append(token.lemma_.lower())
        # Беремо Універсальний POS-тег (NOUN, VERB, ADJ тощо)
        pos_tags.append(token.pos_)
        # Опційно: токен + його POS-тег
        pos_text_pairs.append(f"{token.text}_{token.pos_}")
        
    return {
        "lemma_text": " ".join(lemmas),
        "pos_seq": " ".join(pos_tags),
        "pos_text": " ".join(pos_text_pairs)
    }