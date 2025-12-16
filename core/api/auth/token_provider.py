class TokenProvider:
    _token = None

    @classmethod
    def get_token(cls):
        if cls._token is None:
            cls._token = cls._generate_token()
        return cls._token

    @staticmethod
    def _generate_token():
        # Call auth API here
        return "DUMMY_TOKEN"
