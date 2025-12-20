import reflex as rx
from portal.components.layout import layout


@rx.page(route="/")
def home() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("Bienvenido", size="7"),
            rx.text(
                "Sistema de gestión de documentos. "
                "Desde aquí podrás subir, organizar y consultar documentación.",
                max_width="600px",
            ),
            spacing="4",
            align="start",
        )
    )
