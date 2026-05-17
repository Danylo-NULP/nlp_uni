from spacy.pipeline import EntityRuler

def add_hybrid_rules(nlp):
    """
    Створює гібридний pipeline, додаючи правила для доменних сутностей SNLI 
    (Кольори, Одяг, Тварини).
    """
    # Якщо ruler вже є в пайплайні, видаляємо його для чистоти експерименту
    if "entity_ruler" in nlp.pipe_names:
        nlp.remove_pipe("entity_ruler")
        
    # Додаємо ruler ПЕРЕД стандартним 'ner', щоб наші правила мали пріоритет
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    
    patterns = [
        # Правила для кольорів
        {"label": "COLOR", "pattern": [{"LOWER": {"IN": ["red", "blue", "green", "black", "white", "yellow", "orange", "pink", "brown", "grey", "gray", "purple"]}}]},
        
        # Правила для одягу (включаючи комбінації типу "t-shirt")
        {"label": "CLOTHING", "pattern": [{"LOWER": {"IN": ["shirt", "t-shirt", "hat", "pants", "shorts", "jacket", "dress", "suit", "helmet", "glasses", "shoes", "coat", "jeans"]}}]},
        
        # Правила для тварин
        {"label": "ANIMAL", "pattern": [{"LOWER": {"IN": ["dog", "dogs", "cat", "cats", "horse", "bird", "cow", "sheep", "elephant", "bear", "zebra", "puppy"]}}]}
    ]
    
    ruler.add_patterns(patterns)
    
    return nlp