from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import logging

from function import safe_get, setup_driver

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_kicker_from_link(link):
    """
        Obtiene el kicker dentro del enlace de la noticia de forma paralela
    """
    from function import setup_driver
    try:
        driver = setup_driver()
        driver.get(link)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "volanta"))
        )
        kicker = safe_get(driver, By.CLASS_NAME, "volanta")
        return link, kicker
    except Exception as e:
        logging.warning(f"Error al extraer kicker de {link}: {e}")
        return link, ""
    finally:
        driver.quit()

def extract_articles(driver, url):
    """
        Realiza el scrapping de forma general
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
    pending_links = []

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

            if not kicker and link:
                pending_links.append(link)

        except Exception as e:
            logging.warning(f"Error al extraer un artículo: {e}")
            continue

    # Ejecutar paralelamente la obtención de kickers
    if pending_links:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_link = {executor.submit(get_kicker_from_link, link): link for link in pending_links}
            kicker_results = {}
            for future in as_completed(future_to_link):
                link, kicker = future.result()
                kicker_results[link] = kicker

        # Actualizar el kicker en los artículos
        for article in articles:
            if not article["kicker"] and article["link"] in kicker_results:
                article["kicker"] = kicker_results[article["link"]]

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