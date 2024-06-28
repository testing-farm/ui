import reflex as rx

from tft.ui import State, Token


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
