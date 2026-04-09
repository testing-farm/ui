from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TF_UI",
    settings_files=["settings.yaml"],
    environments=True,
)


def is_mock_login_allowed() -> bool:
    """Check if mock login should be allowed.

    Mock login is only allowed when ALLOW_MOCK_LOGIN is True AND
    the API is running on localhost.
    """
    if settings.current_env != 'development':
        return False

    if not settings.ALLOW_MOCK_LOGIN:
        return False

    api_url = settings.TESTING_FARM_PUBLIC_API.lower()
    if not ('localhost' in api_url or '127.0.0.1' in api_url):
        return False

    return True
