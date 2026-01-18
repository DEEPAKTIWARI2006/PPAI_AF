import json


class TokenProvider:
    _token = None

    @classmethod
    def get_token(cls, api_context):
        if cls._token is None:
            cls._token = cls._generate_token(api_context)
        return cls._token

    @staticmethod
    def _generate_token(api_context):
        response = api_context.post(
            "/auth/login",
            data=json.dumps({"username": "mor_2314", "password": "83r5^_"}),
        )
        token = response.json()["token"]
        return token
