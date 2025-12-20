import reflex as rx

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Gestión Documental", size="5"),
            rx.divider(),
            rx.link("🏠 Home", href="/"),
            rx.link("📄 Subir documento", href="/subir-documento"),
            rx.link("📂 Listar documentos", href="/listar-documentos"),
            spacing="3",
            align="start",
        ),
        width="250px",
        height="100vh",
        padding="1em",
        border_right="1px solid #eaeaea",
    )