#holds the APIClient class, which knows how to fetch data from the API with built-in retries and logging.

import requests          # API lai call garna chahine library
import logging           # used instead of print -- professional logging
import time               # retry huda this works
logger = logging.getLogger(__name__)
class APIClient:
    def __init__(self, base_url: str):
        # when we make APIClient, base_url (keep in mind)(inside self)
        self.base_url = base_url

    def get_users(self, max_retries: int = 3) -> list:
        url = f"{self.base_url}/users"        # made full url for users endpoint
        # loop for three times to try to fetch the data from API
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, timeout=5)   # sending request to API 
                response.raise_for_status()                # stops here if there is error 
                logger.info(f"Fetched users successfully on attempt {attempt}")
                return response.json()                 # successful response, return the JSON data
            except requests.RequestException as e:
                # if request fails, comes here
                logger.warning(f"Attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    # last try fail 
                    logger.error("All retry attempts failed")
                    raise
                time.sleep(2 ** attempt)   # waits and tries again (backoff)