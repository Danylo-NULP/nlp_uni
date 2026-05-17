import spacy

def load_baseline_pipeline(model_name="en_core_web_sm"):
    """
    Завантажує базову модель spaCy. 
    (Модель має бути попередньо завантажена через !python -m spacy download ...)
    """
    # Disable components we don't need to speed up processing
    nlp = spacy.load(model_name, disable=["parser", "lemmatizer"])
    return nlp

def get_entities(doc):
    """
    Повертає список знайдених сутностей у форматі (текст, лейбл).
    """
    return [(ent.text, ent.label_) for ent in doc.ents]