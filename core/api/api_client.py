from playwright.sync_api import APIRequestContext, Playwright
from utils.logger import get_test_logger

class APIClient:
    """
    Playwright-based API client using APIRequestContext
    """

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context
        self.logger = get_test_logger(self.__class__.__name__)

    def get(self, endpoint: str, **kwargs):
        self.logger.info(f"GET {endpoint}")
        response = self.request.get(endpoint, **kwargs)
        return response

    def post(self, endpoint: str, **kwargs):
        self.logger.info(f"POST {endpoint}")
        response = self.request.post(endpoint, **kwargs)
        return response

    def put(self, endpoint: str, **kwargs):
        self.logger.info(f"PUT {endpoint}")
        response = self.request.put(endpoint, **kwargs)
        return response

    def delete(self, endpoint: str, **kwargs):
        self.logger.info(f"DELETE {endpoint}")
        response = self.request.delete(endpoint, **kwargs)
        return response
