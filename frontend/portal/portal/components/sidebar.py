import reflex as rx

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Gestión de Documentos", size="3"),
            rx.divider(),

            rx.link(
                rx.hstack(
                    rx.icon("home", size=12),
                    rx.text("Home"),
                    spacing="2",
                    align="center",
                ),
                href="/",
            ),

            rx.link(
                rx.hstack(
                    rx.icon("folder", size=12),
                    rx.text("Listar documentos"),
                    spacing="2",
                    align="center",
                ),
                href="/listar-documentos",
            ),

            rx.link(
                rx.hstack(
                    rx.icon("file_plus_2", size=12),
                    rx.text("Guardar documento"),
                    spacing="2",
                    align="center",
                ),
                href="/subir-documento",
            ),
            spacing="3",
            align="start",
        ),
        width="250px",
        height="100vh",
        padding="1em",
        border_right="1px solid #eaeaea",
    )