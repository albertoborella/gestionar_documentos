import reflex as rx

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Gestión de Documentos", size="3"),
            rx.divider(),

            rx.link(
                rx.hstack(
                    rx.icon("home", size=18),
                    rx.text("Home"),
                    spacing="2",
                    align="center",
                ),
                href="/",
            ),

            rx.link(
                rx.hstack(
                    rx.icon("folder", size=16),
                    rx.text("Listar documentos"),
                    spacing="2",
                    align="center",
                ),
                href="/listar-documentos",
            ),

            rx.link(
                rx.hstack(
                    rx.icon("signal_medium", size=16),
                    rx.text("Modificar documento"),
                    spacing="2",
                    align="center",
                ),
                href="/modificar-documento",
            ),

            rx.link(
                rx.hstack(
                    rx.icon("filter", size=16),
                    rx.text("Filtrar documentos"),
                    spacing="2",
                    align="center",
                ),
                href="/filtrar-documentos",
            ),

            spacing="3",
            align="start",
        ),
        width="250px",
        height="100vh",
        padding="1em",
        border_right="1px solid #eaeaea",
    )