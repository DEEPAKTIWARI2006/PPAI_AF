import requests
from utils.logger import get_test_logger

class APIClient:
    """
    Generic API client for any REST endpoint.
    """

    def __init__(self, base_url: str, headers: dict = None, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        self.timeout = timeout
        self.logger = get_test_logger(self.__class__.__name__)

    def _request(self, method: str, endpoint: str, **kwargs):
        
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"{method} {url}")

        response = self.session.request(
            method=method,
            url=url,
            timeout=self.timeout,
            **kwargs
        )

        self.logger.info(
            f"Status: {response.status_code}, "
            f"Response: {response.text[:500]}"
        )

        return response

    def get(self, endpoint: str, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)
