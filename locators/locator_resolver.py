class LocatorResolver:

    @staticmethod
    def resolve(template: str, **kwargs) -> str:
        """
        Safely resolves dynamic locator templates.
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing placeholder for locator: {e}")
