import pandas as pd

def compare_pipelines(text, baseline_nlp, hybrid_nlp):
    """
    Проганяє один текст через обидві моделі і повертає порівняльний словник.
    """
    baseline_doc = baseline_nlp(text)
    hybrid_doc = hybrid_nlp(text)
    
    baseline_ents = [(ent.text, ent.label_) for ent in baseline_doc.ents]
    hybrid_ents = [(ent.text, ent.label_) for ent in hybrid_doc.ents]
    
    return {
        "Text": text,
        "Baseline Entities": baseline_ents if baseline_ents else "None",
        "Hybrid Entities": hybrid_ents if hybrid_ents else "None"
    }

def batch_compare(texts, baseline_nlp, hybrid_nlp):
    """
    Генерує DataFrame для порівняння списку текстів (Evaluation Set).
    """
    results = [compare_pipelines(t, baseline_nlp, hybrid_nlp) for t in texts]
    return pd.DataFrame(results)