import pytest
from core.api.api_client import APIClient
from core.api.api_context import APIContext


@pytest.fixture
def api():
    context = APIContext.get_base_context()
    return APIClient(
        base_url=context["base_url"],
        headers=context["headers"]
    )


@pytest.mark.api
def test_get_users(api):
    response = api.get("/books/5")

    assert response.status_code == 200
    # assert isinstance(response.json(), list)


# @pytest.mark.api
# def test_create_user(api):
#     payload = {
#         "name": "John",
#         "email": "john@test.com"
#     }

#     response = api.post("/users", json=payload)
#     assert response.status_code in (200, 201)
