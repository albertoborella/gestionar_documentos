import reflex as rx
from portal.components.layout import layout
from portal.state.documento_state import DocumentoEditState

@rx.page(
    route="/editar-documento/[id]",
    on_load=[
        DocumentoEditState.cargar_enums,
        DocumentoEditState.cargar_documento,
    ],
)
def editar_documento() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Editar Documento",
                font_size="2xl",
                font_weight="bold",
            ),

            # --- Loading ---
            rx.cond(
                DocumentoEditState.loading,
                rx.spinner(size="3"),
            ),

            # --- Error ---
            rx.cond(
                DocumentoEditState.error != "",
                rx.text(
                    DocumentoEditState.error,
                    color="red",
                ),
            ),

            # --- Formulario ---
            rx.cond(
                ~DocumentoEditState.loading,
                rx.vstack(
                    rx.input(
                        placeholder="Título",
                        value=DocumentoEditState.titulo,
                        on_change=DocumentoEditState.set_titulo,
                    ),
                    rx.input(
                        placeholder="Subtítulo",
                        value=DocumentoEditState.subtitulo,
                        on_change=DocumentoEditState.set_subtitulo,
                    ),
                    rx.text_area(
                        placeholder="Descripción",
                        value=DocumentoEditState.descripcion,
                        on_change=DocumentoEditState.set_descripcion,
                    ),
                    rx.select(
                        DocumentoEditState.origenes,
                        placeholder="Origen",
                        value=DocumentoEditState.origen,
                        on_change=DocumentoEditState.set_origen,
                    ),
                    rx.select(
                        DocumentoEditState.secciones,
                        placeholder="Sección",
                        value=DocumentoEditState.seccion,
                        on_change=DocumentoEditState.set_seccion,
                    ),
                    rx.select(
                        DocumentoEditState.estados,
                        placeholder="Estado",
                        value=DocumentoEditState.estado,
                        on_change=DocumentoEditState.set_estado,
                    ),
                    rx.button(
                        "Guardar Cambios",
                        on_click=DocumentoEditState.guardar_cambios,
                        color_scheme="green",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
            ),

            spacing="6",
            width="100%",
            max_width="600px",
            padding="6",
        ),
        width="100%",
    )