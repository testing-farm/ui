import reflex as rx

from tft.ui import State
from tft.ui.pages import (
    home,
    sign_in,
    sign_in_fedora_error,
    sign_in_github_error,
    sign_in_redhat_error,
    signing_in,
    tokens,
)

app = rx.App()
app.add_page(home, route='/', title="Testing Farm")
app.add_page(
    tokens,
    on_load=[State.start_loading_tokens, State.get_tokens, State.rotate_show_created_token_state],
    title="Testing Farm",
    route='/tokens',
)
app.add_page(sign_in, route='/signin', title="Testing Farm")
app.add_page(signing_in, route='/login/github/callback', on_load=State.login_github_callback, title="Testing Farm")
app.add_page(sign_in_github_error, route='/login/github/error', title="Testing Farm")
app.add_page(signing_in, route='/login/fedora/callback', on_load=State.login_fedora_callback, title="Testing Farm")
app.add_page(sign_in_fedora_error, route='/login/fedora/error', title="Testing Farm")
app.add_page(signing_in, route='/login/redhat/callback', on_load=State.login_redhat_callback, title="Testing Farm")
app.add_page(sign_in_redhat_error, route='/login/redhat/error', title="Testing Farm")
