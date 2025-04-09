from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging

from app.function import safe_get, setup_driver

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_articles(driver, url):
    """
    Accede a la página indicada y extrae los artículos.
    Devuelve un DataFrame con: título, antetítulo, imagen, enlace, datetime, y hash_id.
    """
    logging.info(f"Accediendo a: {url}")
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contenedor_dato_modulo"))
        )
    except Exception as e:
        logging.error(f"No se encontraron artículos: {e}")
        return pd.DataFrame()

    articles = []
    news_elements = driver.find_elements(By.CLASS_NAME, "contenedor_dato_modulo")

    for el in news_elements:
        try:
            title = safe_get(el, By.CLASS_NAME, "titulo")
            kicker = safe_get(el, By.CLASS_NAME, "volanta")
            image = safe_get(el, By.TAG_NAME, "img", "src")
            link = safe_get(el, By.TAG_NAME, "a", "href")

            articles.append({
                "title": title,
                "kicker": kicker,
                "image": image,
                "link": link
            })

        except Exception as e:
            logging.warning(f"Error al extraer un artículo: {e}")
            continue

    return pd.DataFrame(articles)

def run_scraper(url):
    """
    Ejecuta el scraper y devuelve los resultados en un DataFrame.
    """
    driver = setup_driver()
    try:
        return extract_articles(driver, url)
    finally:
        driver.quit()