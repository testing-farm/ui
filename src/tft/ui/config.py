import socket
from ipaddress import ip_address

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TF_UI",
    settings_files=["settings.yaml"],
    environments=True,
)


def is_mock_login_allowed() -> bool:
    """Check if mock login should be allowed.

    Mock login is only allowed when ALLOW_MOCK_LOGIN is True AND
    the API is running on localhost AND the machine hostname indicates
    a local environment.
    """
    if not settings.ALLOW_MOCK_LOGIN:
        return False

    api_url = settings.TESTING_FARM_PUBLIC_API.lower()
    if not ('localhost' in api_url or '127.0.0.1' in api_url):
        return False

    # Check hostname to ensure we're running locally
    hostname = socket.gethostname()
    if hostname != 'localhost':
        return False

    try:
        ipaddr = ip_address(hostname)
        if ipaddr.is_link_local:
            return True
    except ValueError:
        # hostname is not an IP address, which is expected for most systems
        pass

    return True
