from . import processor_init, scraper_init

if __name__ == "__main__":
      df_scraped = scraper_init()
      processor_init(df_scraped)