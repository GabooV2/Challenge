import hashlib
from datetime import datetime, timezone
import re

def clean_text(text):
    """
    Limpia y estandariza un texto eliminando espacios y caracteres innecesarios.
    """
    if not isinstance(text, str):
        return ""
    text = text.replace('\n', ' ').replace('\r', '')
    return re.sub(r'\s+', ' ', text.strip())

def generate_id(row):
    """
    Genera un hash único combinando título y link.
    """
    unique_str = row['title'] + row['link']
    return hashlib.md5(unique_str.encode()).hexdigest()

def process_articles(df):
    """
    Recibe un DataFrame crudo y devuelve uno limpio y listo para ingestión.
    """
    df = df.drop_duplicates(subset=["title", "link"])

    df['title'] = df['title'].apply(clean_text)
    df['kicker'] = df['kicker'].apply(clean_text)
    df['source'] = "yogonet.com"

    df = df[df['title'].notna() & df['link'].notna()]

    # Métricas solicitadas
    df['word_count'] = df['title'].apply(lambda x: len(x.split()))
    df['char_count'] = df['title'].apply(len)
    df['capitalized_words'] = df['title'].apply(
        lambda x: [w for w in x.split() if w.istitle()]
    )

    df['scraped_at'] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    df['id'] = df.apply(generate_id, axis=1)

    return df
