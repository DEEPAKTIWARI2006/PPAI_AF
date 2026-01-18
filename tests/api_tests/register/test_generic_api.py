import pytest
from core.api.api_client import APIClient
from core.api.api_context import APIContext


@pytest.fixture(scope="session")
def api_public(playwright_instance):
    ctx = APIContext.public_context(playwright_instance)
    yield APIClient(ctx)
    ctx.dispose()


@pytest.fixture(scope="session")
def api_auth(playwright_instance):
    ctx = APIContext.authenticated_context(playwright_instance)
    yield APIClient(ctx)
    ctx.dispose()


@pytest.mark.api
def test_create_user(api_auth):
    response = api_auth.get("carts/user/2")
    assert response.status == 200
