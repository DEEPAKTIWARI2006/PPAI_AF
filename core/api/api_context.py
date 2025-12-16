from core.config_loader import ConfigLoader


class APIContext:
    """
    Provides API base configuration.
    """

    @staticmethod
    def get_base_context():
        return {
            "base_url": ConfigLoader.get_api_base_url(),
            "headers": {
                "Content-Type": "application/json"
            }
        }
