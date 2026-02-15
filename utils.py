import requests
import time
import logging
import os


logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_with_retry(url, retries=3):
    for i in range(retries):
        try:
            headers = {"Authorization": os.getenv("PEXELS_KEY")}
            r = requests.get(url, headers=headers, timeout=10)

            r.raise_for_status()
            return r.json()
        except Exception as e:
            logging.error(f"Retry {i+1}: {e}")
            time.sleep(2)

    return None
