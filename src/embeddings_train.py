from gensim.models import Word2Vec, FastText
import multiprocessing

def train_word2vec(tokenized_sentences, vector_size=100, window=5, min_count=3, sg=1):
    """
    Тренує модель Word2Vec на наданому корпусі.
    sg=1 означає використання архітектури Skip-gram (зазвичай краще для семантики),
    sg=0 - CBOW (швидше, краще для частих слів).
    """
    cores = multiprocessing.cpu_count()
    
    model = Word2Vec(
        sentences=tokenized_sentences,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        sg=sg,
        workers=cores,
        seed=42
    )
    return model

def train_fasttext(tokenized_sentences, vector_size=100, window=5, min_count=3, sg=1):
    """
    Тренує модель FastText на наданому корпусі.
    FastText враховує символьні n-грами, що допомагає з OOV (out-of-vocabulary) 
    словами та морфологією.
    """
    cores = multiprocessing.cpu_count()
    
    model = FastText(
        sentences=tokenized_sentences,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        sg=sg,
        workers=cores,
        seed=42
    )
    return model