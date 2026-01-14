import logging
import time
from datetime import date, datetime
from typing import Optional

import jwt
import reflex as rx
import requests

from tft.ui.config import settings

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class AuthorizedUser(rx.Base):
    auth_id: str
    auth_method: str
    auth_name: str
    ranch: list[str]
    role: str
    exp: int

    def is_expired(self) -> bool:
        return self.exp < time.time()


class Token(rx.Base):
    id: str
    name: str
    ranch: Optional[str]
    role: str
    created: datetime
    expiration_date: Optional[date] = None


class TokenCreated(Token):
    api_key: str


def _get_error_message(response: requests.Response) -> str:
    """Extract error message from API response."""
    try:
        data = response.json()
        if isinstance(data, dict) and 'message' in data:
            return data['message']
    except ValueError:
        # Raised if response is not JSON-decodable
        pass
    return response.text


class State(rx.State):
    access_token: str = rx.LocalStorage()
    # refresh_token: str = rx.LocalStorage()  # TODO
    authorized_user: AuthorizedUser | None = None
    tokens: list[Token] = []
    tokens_loaded: bool = False
    created_token: TokenCreated | None = None
    create_token_form_token_name: str = ''
    create_token_form_expiration_date: str = ''

    # 0 - do not do anything, stay hidden
    # 1 - just created, should be shown
    # 2 - currently being shown
    show_created_token_state: int = 0

    def login_github_callback(self):
        logging.info('attempting to login via github')
        if not "code" in self.router.page.params:
            return rx.redirect('/signin')

        response = requests.get(
            f'{settings.TESTING_FARM_PUBLIC_API}/v0.1/login/github/callback?code={self.router.page.params["code"]}'
        )

        if response.status_code != 200:
            return rx.redirect('/login/github/error')

        logging.info(f'{response=}')
        self.access_token = response.text
        jwt_decoded = jwt.decode(self.access_token, options={"verify_signature": False})
        self.authorized_user = AuthorizedUser(**jwt_decoded)
        logging.info(f'{self.access_token=} {self.authorized_user=}')
        return rx.redirect('/tokens')

    def login_fedora_callback(self):
        logging.info('attempting to login via fedora')
        if not "code" in self.router.page.params:
            return rx.redirect('/signin')

        response = requests.get(
            f'{settings.TESTING_FARM_PUBLIC_API}/v0.1/login/fedora/callback?code={self.router.page.params["code"]}'
        )

        if response.status_code != 200:
            return rx.redirect('/login/fedora/error')

        logging.info(f'{response=}')
        self.access_token = response.text
        jwt_decoded = jwt.decode(self.access_token, options={"verify_signature": False})
        self.authorized_user = AuthorizedUser(**jwt_decoded)
        logging.info(f'{self.access_token=} {self.authorized_user=}')
        return rx.redirect('/tokens')

    def login_redhat_callback(self):
        logging.info('attempting to login via redhat')
        if not "code" in self.router.page.params:
            return rx.redirect('/signin')

        response = requests.get(
            f'{settings.TESTING_FARM_PUBLIC_API}/v0.1/login/redhat/callback?code={self.router.page.params["code"]}'
        )

        if response.status_code != 200:
            return rx.redirect('/login/redhat/error')

        logging.info(f'{response=}')
        self.access_token = response.text
        jwt_decoded = jwt.decode(self.access_token, options={"verify_signature": False})
        self.authorized_user = AuthorizedUser(**jwt_decoded)
        logging.info(f'{self.access_token=} {self.authorized_user=}')
        return rx.redirect('/tokens')

    def login_mock_callback(self):
        logging.info('attempting to login via mock')

        response = requests.get(f'{settings.TESTING_FARM_PUBLIC_API}/v0.1/login/mock')

        if response.status_code != 200:
            return rx.redirect('/login/mock/error')

        logging.info(f'{response=}')
        self.access_token = response.text
        jwt_decoded = jwt.decode(self.access_token, options={"verify_signature": False})
        self.authorized_user = AuthorizedUser(**jwt_decoded)
        logging.info(f'{self.access_token=} {self.authorized_user=}')
        return rx.redirect('/tokens')

    def logout(self):
        rx.remove_local_storage('access_token')
        self.authorized_user = None
        return rx.redirect('/')

    @rx.var
    def is_user_logged_in(self) -> bool:
        return self.authorized_user is not None and not self.authorized_user.is_expired()

    def start_loading_tokens(self) -> None:
        self.tokens_loaded = False

    def get_tokens(self):
        if self.is_user_logged_in:
            response = requests.get(
                f'{settings.TESTING_FARM_PUBLIC_API}/v0.1/tokens',
                headers={'Authorization': f'Bearer {self.access_token}'},
            )
            self.tokens_loaded = True

            if response.status_code != 200:
                return rx.toast(
                    f"Error {response.status_code} while fetching tokens: {_get_error_message(response)}",
                    level="error",
                    duration=20000,
                )

            self.tokens = [Token(**token) for token in response.json()]
            self.tokens.sort(key=lambda t: t.created, reverse=True)

    def create_token(self, form_data):
        if 'role' not in form_data:
            form_data.update({'role': 'user'})

        # Set expiration_date to null if not provided
        if not form_data.get('expiration_date'):
            form_data['expiration_date'] = None

        response = requests.post(
            f'{settings.TESTING_FARM_PUBLIC_API}/v0.1/tokens',
            json=form_data,
            headers={'Authorization': f'Bearer {self.access_token}'},
        )

        if response.status_code != 200:
            return rx.toast(
                f"Error {response.status_code} while creating token: {_get_error_message(response)}",
                level="error",
                duration=20000,
            )

        self.created_token = TokenCreated(**response.json())
        self.show_created_token_state = 1
        return rx.redirect('/tokens')

    @rx.var
    def create_token_form_invalid(self) -> bool:
        return len(self.create_token_form_token_name) == 0

    def delete_token(self, token_id: str):
        response = requests.delete(
            f'{settings.TESTING_FARM_PUBLIC_API}/v0.1/tokens/{token_id}',
            headers={'Authorization': f'Bearer {self.access_token}'},
        )

        if response.status_code != 200:
            return rx.toast(
                f"Error deleting token: {_get_error_message(response)}",
                level="error",
                duration=20000,
            )

        self.tokens = [token for token in self.tokens if token.id != token_id]
        return rx.toast(f"Token {token_id} was successfully deleted.", level="success")

    def rotate_show_created_token_state(self):
        if self.show_created_token_state == 1:
            self.show_created_token_state = 2
        elif self.show_created_token_state == 2:
            self.show_created_token_state = 0

    @rx.var
    def ranch_redhat_allowed(self) -> bool:
        if self.authorized_user and self.authorized_user.ranch:
            return 'redhat' in self.authorized_user.ranch
        return False

    @rx.var
    def ranch_public_allowed(self) -> bool:
        if self.authorized_user and self.authorized_user.ranch:
            return 'public' in self.authorized_user.ranch
        return False

    @rx.var
    def role_admin(self) -> bool:
        if self.authorized_user:
            return 'admin' in self.authorized_user.role
        return False

    @rx.var
    def show_created_token(self) -> bool:
        return self.show_created_token_state == 2
