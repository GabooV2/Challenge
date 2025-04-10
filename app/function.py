from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(headless=True):
    """
    Configura el driver de Selenium para usar Chrome.
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def safe_get(element, by, value, attr=None):
    """
    Intenta obtener el texto o atributo de un subelemento, o devuelve string vacío.
    """
    try:
        found = element.find_element(by, value)
        return found.get_attribute(attr).strip() if attr else found.text.strip()
    except:
        return ""
    
def save_to_csv(data, origin=None):
      """Guarda los datos completos en un archivo CSV."""
      try:
            if origin =="scraper":
                  file = "data\\raw\\"
                  filename = "news_raw"
            elif origin =="processor":
                  file = "data\\processed\\"
                  filename = "news_processed"
            else:
                 file = "data\\"
                 filename = "news"

            date = datetime.today().strftime("%Y-%m-%d")
            path = f"{file}{filename}_{date}.csv"
            data.to_csv(path, index=False, quotechar='"')  
            print(f"Datos guardados en {path}")
      except Exception as e:
            print(f"Error al guardar el archivo CSV: {str(e)}")