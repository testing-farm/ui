import reflex as rx

from tft.ui import State
from tft.ui.pages import home, sign_in, signing_in, tokens, user_settings

app = rx.App()
app.add_page(home, route='/', title="Testing Farm")
app.add_page(
    tokens,
    on_load=[State.start_loading_tokens, State.get_tokens, State.rotate_show_created_token_state],
    title="Testing Farm",
    route='/tokens',
)
app.add_page(sign_in, route='/signin', title="Testing Farm")
app.add_page(user_settings, route='/settings', title="Testing Farm")
app.add_page(signing_in, route='/login/github/callback', on_load=State.login_github_callback)
app.add_page(signing_in, route='/login/fedora/callback', on_load=State.login_fedora_callback)
