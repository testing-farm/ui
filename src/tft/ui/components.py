import reflex as rx

from tft.ui import State, Token


def navbar() -> rx.Component:
    return rx.fragment(
        rx.hstack(
            rx.box(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="https://gitlab.com/uploads/-/system/group/avatar/5515434/tft-logo.png",
                            width="64px",
                            height="auto",
                        ),
                        href='/',
                    ),
                    rx.link(rx.text('Home', size="5", weight="medium"), href='/'),
                    rx.link(
                        rx.hstack(
                            rx.text('Docs', size="5", weight="medium"),
                            rx.icon(tag='external-link', size=20),
                            spacing='2',
                            align_items='center',
                        ),
                        href='https://docs.testing-farm.io/',
                        is_external=True,
                    ),
                    rx.link(
                        rx.hstack(
                            rx.text('API', size="5", weight="medium"),
                            rx.icon(tag='external-link', size=20),
                            spacing='2',
                            align_items='center',
                        ),
                        href='https://api.testing-farm.io/',
                        is_external=True,
                    ),
                    spacing="8",
                    align_items="center",
                ),
                margin="32px",
            ),
            rx.box(
                rx.cond(
                    State.is_hydrated,
                    rx.cond(
                        State.is_user_logged_in,
                        rx.drawer.root(
                            rx.drawer.trigger(
                                rx.button(rx.icon(tag="circle-user-round", size=40), variant="ghost", round="full")
                            ),
                            rx.drawer.overlay(z_index="5"),
                            rx.drawer.portal(
                                rx.drawer.content(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.color_mode.button(),
                                            rx.box(
                                                rx.drawer.close(
                                                    rx.box(rx.button(rx.icon(tag="x", size=20), variant='ghost'))
                                                ),
                                                align='end',
                                            ),
                                            align_items="center",
                                            width="100%",
                                            justify="between",
                                        ),
                                        rx.text(
                                            f'Signed in as {State.authorized_user.auth_name} via '
                                            f'{State.authorized_user.auth_method}.'
                                        ),
                                        rx.link(
                                            rx.flex(rx.icon(tag="key-round"), rx.text('Your Tokens'), spacing='2'),
                                            href='/tokens',
                                        ),
                                        rx.link(
                                            rx.flex(rx.icon(tag="log-out"), rx.text('Sign out'), spacing='2'),
                                            on_click=State.logout,
                                        ),
                                    ),
                                    height="100%",
                                    width="250px",
                                    padding="24px",
                                    background_color=rx.color_mode_cond(light="white", dark="black"),
                                    direction="column",
                                    left='calc(100% - 250px);',
                                ),
                            ),
                            direction="right",
                        ),
                        rx.link(rx.button('Sign in', width="150px"), href='/signin'),
                    ),
                ),
                align="end",
                margin="32px",
            ),
            justify="between",
            align_items="center",
        ),
        rx.divider(),
    )


def create_token_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(
                rx.icon(tag="plus"),
                "Create a new token",
                color_scheme="green",
                on_click=State.set_create_token_form_token_name(''),
            )
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Create a new token"),
            rx.alert_dialog.description(
                rx.form.root(
                    rx.form.field(
                        rx.flex(
                            rx.form.label("Token name"),
                            rx.input(name="name", on_change=State.set_create_token_form_token_name),
                            rx.cond(
                                State.create_token_form_invalid,
                                rx.form.message("Token name cannot be empty.", color="var(--red-11)"),
                            ),
                            rx.form.label("Ranch"),
                            rx.select.root(
                                rx.select.trigger(),
                                rx.select.content(
                                    rx.select.group(
                                        rx.cond(State.ranch_public_allowed, rx.select.item('Public', value='public')),
                                        rx.cond(State.ranch_redhat_allowed, rx.select.item('Red Hat', value='redhat')),
                                    ),
                                ),
                                default_value='public',
                                name="ranch",
                            ),
                            rx.cond(
                                State.role_admin,
                                rx.fragment(
                                    rx.form.label("Role"),
                                    rx.select.root(
                                        rx.select.trigger(),
                                        rx.select.content(
                                            rx.select.group(
                                                rx.select.item('User', value='user'),
                                                rx.select.item('Worker', value='worker'),
                                                rx.select.item('Admin', value='admin'),
                                            ),
                                        ),
                                        default_value='user',
                                        name="role",
                                    ),
                                ),
                            ),
                            rx.hstack(
                                rx.alert_dialog.cancel(rx.button("Cancel", color_scheme="gray")),
                                rx.form.submit(
                                    rx.button("Submit", color_scheme="green", disabled=State.create_token_form_invalid),
                                    as_child=True,
                                ),
                            ),
                            direction="column",
                            spacing="2",
                            align="stretch",
                        ),
                    ),
                    on_submit=State.create_token,
                    reset_on_submit=True,
                ),
            ),
        ),
    )


def token_table_row(token: Token):
    return rx.table.row(
        rx.table.row_header_cell(token.id),
        rx.table.cell(token.name),
        rx.table.cell(token.ranch),
        rx.table.cell(token.role),
        rx.table.cell(rx.moment(token.created, format="YYYY-MM-DD HH:mm:ss")),
        rx.table.cell(
            rx.hstack(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(rx.button(rx.icon(tag="trash-2", size=20), color_scheme="red", size="1")),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Delete token"),
                        rx.alert_dialog.description(
                            "Are you sure? This action cannot be undone, you token will stop working immediatelly.",
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("ID"),
                                        rx.table.column_header_cell("Name"),
                                        rx.table.column_header_cell("Ranch"),
                                        rx.table.column_header_cell("Role"),
                                        rx.table.column_header_cell("Created"),
                                    )
                                ),
                                rx.table.body(
                                    rx.table.row(
                                        rx.table.row_header_cell(token.id),
                                        rx.table.cell(token.name),
                                        rx.table.cell(token.ranch),
                                        rx.table.cell(token.role),
                                        rx.table.cell(rx.moment(token.created, format="YYYY-MM-DD HH:mm:ss")),
                                    )
                                ),
                            ),
                        ),
                        rx.flex(
                            rx.alert_dialog.cancel(
                                rx.button(
                                    "Cancel",
                                    color_scheme="gray",
                                ),
                            ),
                            rx.alert_dialog.action(
                                rx.alert_dialog.action(
                                    rx.button(
                                        "Delete token",
                                        color_scheme="red",
                                        variant="solid",
                                        on_click=State.delete_token(token.id),
                                    ),
                                ),
                            ),
                            spacing="3",
                        ),
                    ),
                )
            )
        ),
    )
