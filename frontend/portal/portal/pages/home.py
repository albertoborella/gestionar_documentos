import reflex as rx
from portal.components.layout import layout

@rx.page(route="/")
def home() -> rx.Component:
    return layout(
        rx.center(
            rx.vstack(
                rx.heading("Bienvenido", size="7"),
                rx.text(
                    "Sistema de gestión de documentos. "
                    "Desde aquí podrás filtrar y consultar documentación que deses",
                ),
                spacing="4",
                align="center",
            ),
            width="100%",
        )
    )
