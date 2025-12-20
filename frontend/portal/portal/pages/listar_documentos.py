import reflex as rx
from portal.components.layout import layout

@rx.page(route="/listar-documentos")
def listar_documentos() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading("Listado de documentos", size="6"),
            rx.text("Documentos cargados en el sistema."),
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.text("Contrato proveedor", font_weight="bold"),
                        rx.text("2025-01-10", color="gray"),
                        justify="between",
                        width="100%",
                    ),
                    rx.text("Sección: Contratos"),
                    padding="1em",
                    border="1px solid #eaeaea",
                    border_radius="8px",
                    width="100%",
                ),
                rx.box(
                    rx.hstack(
                        rx.text("Auditoría interna", font_weight="bold"),
                        rx.text("2025-02-03", color="gray"),
                        justify="between",
                        width="100%",
                    ),
                    rx.text("Sección: Auditorías"),
                    padding="1em",
                    border="1px solid #eaeaea",
                    border_radius="8px",
                    width="100%",
                ),
                spacing="3",
                width="100%",
                max_width="800px",
            ),
            spacing="4",
            align="start",
        )
    )