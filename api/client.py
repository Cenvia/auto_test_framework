import requests
import logging
from config.settings import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or Config.API_BASE_URL
        self.session = requests.Session()
        # 设置超时，防止Windows下卡住
        self.session.timeout = 10

    def get(self, endpoint, params=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params, **kwargs)
        logger.info(f"Response status: {response.status_code}")
        return response

    def post(self, endpoint, data=None, json=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"POST {url}")
        response = self.session.post(url, data=data, json=json, **kwargs)
        logger.info(f"Response status: {response.status_code}")
        return response