import reflex as rx

from tft.ui import State
from tft.ui.components import create_token_dialog, navbar, token_table_row
from tft.ui.config import settings


def tokens() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
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
        ),
    )


def sign_in() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading('Sign in with SSO'),
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
                align_items="center",
            ),
        ),
    )


def signing_in() -> rx.Component:
    return rx.container(rx.text('Signing in...'))


def sign_in_github_error() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.heading('Error signing in via GitHub account'),
            rx.flex(
                rx.text('You must be an admin in the'),
                rx.link('testing-farm', href='https://github.com/orgs/testing-farm', is_external=True),
                rx.text('organization.'),
                spacing='1',
            ),
            rx.flex(
                rx.text('Go to'),
                rx.link(
                    rx.text('Testing Farm onboarding docs'),
                    href='https://docs.testing-farm.io/Testing%20Farm/0.1/onboarding.html',
                    is_external=True,
                ),
                rx.text('for more information.'),
                spacing='1',
            ),
        ),
    )


def sign_in_fedora_error() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.heading('Error signing in via Fedora account'),
            rx.flex(
                rx.text('You must be a part of either'),
                rx.link(
                    'testing-farm', href='https://accounts.fedoraproject.org/group/testing-farm/', is_external=True
                ),
                rx.text('or'),
                rx.link(
                    'fedora-contributor',
                    href='https://accounts.fedoraproject.org/group/fedora-contributor/',
                    is_external=True,
                ),
                rx.text('group.'),
                spacing='1',
            ),
            rx.flex(
                rx.text('Go to'),
                rx.link(
                    rx.text('Testing Farm onboarding docs'),
                    href='https://docs.testing-farm.io/Testing%20Farm/0.1/onboarding.html',
                    is_external=True,
                ),
                rx.text('for more information.'),
                spacing='1',
            ),
        ),
    )


def home() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.flex(
                rx.heading('Welcome to Testing Farm!', align='center', size='8'),
                rx.text(
                    'Testing Farm is a reliable and scalable Testing System as a Service for Red Hat internal services, Red Hat Hybrid Cloud services, and open source projects related to Red Hat products. It is commonly used as a test execution back-end of other services or CI systems. Thanks to its HTTP API it can be easily integrated into any other service.',
                    align='center',
                    size='4',
                ),
                rx.text(
                    'The tests are abstracted away from the test infrastructure using open-source test metadata format which unifies how Red Hat engineers, upstream developers, contributors, and communities are able to discover, debug and run tests.',
                    align='center',
                    size='4',
                ),
                rx.text(
                    'Thanks to the test infrastructure abstraction, the tests can ask for specific hardware requirements for their execution, without worrying about which infrastructure they should use. This abstraction also provides transparent provisioning for users of various infrastructure providers.',
                    align='center',
                    size='4',
                ),
                rx.center(
                    rx.link(
                        rx.button('Get Started', size='4'),
                        href='https://docs.testing-farm.io/Testing%20Farm/0.1/onboarding.html',
                        is_external=True,
                    )
                ),
                direction='column',
                spacing='3',
            ),
        ),
    )
