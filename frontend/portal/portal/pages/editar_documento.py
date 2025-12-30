import reflex as rx
from portal.components.layout import layout
from portal.state.documento_state import DocumentoEditState

@rx.page(route="/documentos/editar/[documento_id]",
         on_load=DocumentoEditState.cargar_documento,
         )
def editar_documento() -> rx.Component:
    return rx.vstack(

        rx.heading("Editar Documento", font_size="2xl", font_weight="bold"),
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
            value=DocumentoEditState.origen,
            on_change=DocumentoEditState.set_origen,    
        ),
        rx.select(
            DocumentoEditState.secciones,
            value=DocumentoEditState.seccion,
            on_change=DocumentoEditState.set_seccion,    
        ),
        rx.select(
            DocumentoEditState.estados,
            value=DocumentoEditState.estado,
            on_change=DocumentoEditState.set_estado,    
        ),
        rx.button(
            "Guardar Cambios",
            on_click=DocumentoEditState.guardar_cambios,
            color_scheme="green",
        ),
        rx.cond(
            DocumentoEditState.loading,
            rx.spinner(),
        ),
        rx.cond(
            DocumentoEditState.error != "",
            rx.text(DocumentoEditState.error, color="red"),
        ),
    )