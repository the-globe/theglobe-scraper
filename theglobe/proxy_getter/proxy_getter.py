#proxy_getter/proxy_getter.py

import requests
import json
import logging
from pathlib import Path


class UpdateProxyList():
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        try:
            proxy_list_dir = Path("theglobe/settings/")
            proxy_list = proxy_list_dir / "proxies.txt"

            url = 'https://www.proxy-list.download/api/v1/get?type=https'

            response = requests.get(url)
            with open(proxy_list, "w") as f:
                f.write(response.text)
            self.logger.info("Updated list of proxies.")

        except Exception as e:
            self.logger.info(f"Unable to update list of proxies because of: {e}")
