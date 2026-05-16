import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "parser", "lemmatizer", "textcat"])
    nlp.enable_pipe("senter")
except OSError:
    import warnings
    warnings.warn("Модель 'en_core_web_sm' не знайдена")
    nlp = None

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<(?!URL>|EMAIL>|PHONE>)[^>]+>', ' ', text)
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def normalize_text(text: str) -> str:
    text = re.sub(r"[‘’`´]", "'", text)
    text = re.sub(r'[“”«»]', '"', text)
    text = re.sub(r'[–—]', '-', text)
    return text

def mask_pii(text: str) -> str:
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', '<EMAIL>', text)
    text = re.sub(r'https?://\S+|www\.\S+', '<URL>', text)
    text = re.sub(r'\+?\b\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', '<PHONE>', text)
    return text

def sentence_split(text: str) -> list[str]:
    if not text or not nlp:
        return []
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

def preprocess(text: str) -> dict:
    cleaned = clean_text(text)
    masked = mask_pii(cleaned)
    normalized = normalize_text(masked)
    sentences = sentence_split(normalized)
    
    return {
        "clean": normalized,
        "sentences": sentences
    }