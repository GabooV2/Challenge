import logging
from app.bq_loader import upload_to_bigquery
from app.function import save_to_csv
from app.scraper import run_scraper, setup_driver, extract_articles
from app.processor import process_articles
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()

def scraper_init():
    """
        Función inicial del proceso de webscraping
    """
    # Scraping
    print("Iniciando scraping...")
    url = os.getenv("URL")
    df_raw = run_scraper(url)
    save_to_csv(df_raw, "scraper")
    if not df_raw.empty:
        print(f"Artículos extraídos: {len(df_raw)}")
        logging.info("Scraping completado y CSV guardado.")
        return df_raw
    else:
        logging.warning("No se extrajeron artículos.")

def processor_init(df_scraped):
    """
        Función inicial para la transformación de los datos extraído
    """
    # Procesamiento
    print("=" * 50)
    print("Procesando artículos...")
    df_clean = process_articles(df_scraped)
    save_to_csv(df_clean, "processor")
    if not df_clean.empty:
        print(f"Artículos procesados: {len(df_clean)}")
        logging.info("Scraping completado y CSV guardado.")
        return df_clean
    else:
        logging.warning("No se extrajeron artículos.")

if __name__ == "__main__":
      """
        Llamada a las función principales para la ejecución del proceso
      """
      df_scraped = scraper_init()
      df_clean = processor_init(df_scraped)
      upload_to_bigquery(df_clean)