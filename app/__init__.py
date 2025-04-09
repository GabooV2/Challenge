import logging
from app.function import save_to_csv
from app.scraper import run_scraper, setup_driver, extract_articles
from app.processor import process_articles
# from bigquery_uploader import upload_to_bigquery
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()

def scraper_init():
    # Scraping
    print("🚀 Iniciando scraping...")
    url = os.getenv("URL")
    df_raw = run_scraper(url)
    save_to_csv(df_raw, "scraper")
    if not df_raw.empty:
        print(f"🔍 Artículos extraídos: {len(df_raw)}")
        logging.info("Scraping completado y CSV guardado.")
        return df_raw
    else:
        logging.warning("No se extrajeron artículos.")

def processor_init(df_scraped):
    # Procesamiento
    print("=" * 50)
    print("🧼 Procesando artículos...")
    df_clean = process_articles(df_scraped)
    save_to_csv(df_clean, "processor")
    if not df_clean.empty:
        print(f"✅ Artículos procesados: {len(df_clean)}")
        logging.info("Scraping completado y CSV guardado.")
        return df_clean
    else:
        logging.warning("No se extrajeron artículos.")