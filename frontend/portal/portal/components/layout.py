import reflex as rx
from portal.components.sidebar import sidebar


def layout(content: rx.Component) -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.box(
            content,
            padding="2em",
            width="100%",
        ),
        width="100%",
        height="100vh",
    )