import reflex as rx

from tft.ui import State
from tft.ui.components import create_token_dialog, token_table_row
from tft.ui.config import settings


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.hstack(
            rx.container(
                rx.hstack(
                    rx.image(
                        src="https://gitlab.com/uploads/-/system/group/avatar/5515434/tft-logo.png",
                        width="64px",
                        height="auto",
                    ),
                    rx.heading("Testing Farm", size="7"),
                    align="center",
                ),
            ),
            rx.vstack(
                rx.cond(
                    State.is_hydrated,
                    rx.cond(
                        ~State.is_user_logged_in,
                        rx.vstack(
                            rx.link(
                                rx.button(
                                    rx.image(src="/fedora.png", width="24px", height="auto"),
                                    "Sign in with Fedora",
                                    width="300px",
                                ),
                                href=f"{settings.TESTING_FARM_PUBLIC_API}/v0.1/login/fedora",
                            ),
                            rx.link(
                                rx.button(
                                    rx.icon(tag="github"),
                                    "Sign in as admin with GitHub",
                                    width="300px",
                                    variant="ghost",
                                ),
                                href=f"{settings.TESTING_FARM_PUBLIC_API}/v0.1/login/github",
                            ),
                        ),
                        rx.fragment(
                            rx.hstack(
                                rx.text(
                                    f'Signed in as {State.authorized_user.auth_name} via '
                                    f'{State.authorized_user.auth_method}.'
                                ),
                                rx.button('Sign out', on_click=State.logout),
                                align="center",
                            ),
                        ),
                    ),
                ),
                align="end",
            ),
            align="center",
        ),
        rx.divider(),
        rx.cond(
            State.is_hydrated,
            rx.cond(
                State.is_user_logged_in,
                rx.cond(
                    State.tokens_loaded,
                    rx.vstack(
                        rx.heading("Your API Tokens", size="5"),
                        rx.cond(
                            State.show_created_token,
                            rx.callout(
                                rx.vstack(
                                    "Your token was successfully created. Make sure to copy it now, "
                                    "it won't be shown again.",
                                    rx.table.root(
                                        rx.table.header(
                                            rx.table.row(
                                                rx.table.column_header_cell("API Token"),
                                            ),
                                            align="center",
                                        ),
                                        rx.table.body(
                                            rx.table.row(
                                                rx.table.row_header_cell(State.created_token.api_key),
                                            ),
                                            align="center",
                                        ),
                                    ),
                                    align="center",
                                ),
                                icon="check",
                                color_scheme="green",
                                high_contrast=True,
                                align="center",
                            ),
                        ),
                        create_token_dialog(),
                        rx.cond(
                            State.tokens,
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("ID"),
                                        rx.table.column_header_cell("Name"),
                                        rx.table.column_header_cell("Ranch"),
                                        rx.table.column_header_cell("Role"),
                                        rx.table.column_header_cell("Created"),
                                        rx.table.column_header_cell("Delete"),
                                    ),
                                ),
                                rx.table.body(rx.foreach(State.tokens, token_table_row)),
                                width="100%",
                            ),
                            rx.text("You don't have any tokens."),
                        ),
                    ),
                    rx.text('Loading tokens...'),
                ),
            ),
        ),
        width="100%",
    )


def signing_in() -> rx.Component:
    return rx.container(rx.text('Signing in...'))
