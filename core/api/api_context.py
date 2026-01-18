from playwright.sync_api import Playwright
from core.config_loader import ConfigLoader
from core.api.auth.token_provider import TokenProvider


class APIContext:

    @staticmethod
    def public_context(playwright):
        return playwright.request.new_context(
            base_url=ConfigLoader.get_api_base_url(),
            extra_http_headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

    @staticmethod
    def authenticated_context(playwright):
        temp = APIContext.public_context(playwright)
        token = TokenProvider.get_token(temp)
        temp.dispose()

        return playwright.request.new_context(
            base_url=ConfigLoader.get_api_base_url(),
            extra_http_headers={"Authorization": f"Bearer {token}"},
        )
