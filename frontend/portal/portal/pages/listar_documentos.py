import reflex as rx
from portal.components.layout import layout
from portal.state.documento_state import DocumentosState


def fila_documento(doc):
    return rx.table.row(
        rx.table.row_header_cell(doc.titulo),
        rx.table.cell(doc.subtitulo),
        rx.table.cell(doc.seccion),
        rx.table.cell(doc.descripcion),
        rx.table.cell(doc.origen),
        rx.table.cell(doc.estado),
        rx.table.cell(
            rx.link(
                "Abrir",
                href=f"http://127.0.0.1:8001/{doc.ruta}",
                is_external=True,
            )
        ),
    )


@rx.page(
    route="/listar-documentos",
    on_load=[
        DocumentosState.cargar_enums,
        DocumentosState.buscar,
    ]
)
def listar_documentos() -> rx.Component:
    #return layout(
    return rx.cond(
            DocumentosState.loading,
            rx.center(rx.spinner()),
            rx.cond(
                DocumentosState.error != "",
                rx.text(
                    DocumentosState.error,
                    color="red",
                ),

                rx.vstack(
                rx.link("Volver al menú >", href="/"),
                rx.text("Listado de Documentos", font_size="2xl", font_weight="bold"),

                # 🔎 FILTROS
                rx.hstack(
                    rx.input(
                        placeholder="Buscar texto…",
                        value=DocumentosState.texto,
                        on_change=DocumentosState.set_texto,
                        width="250px",
                    ),
                    rx.select(
                        DocumentosState.origenes,
                        placeholder="Origen",
                        value=DocumentosState.origen,
                        on_change=DocumentosState.set_origen,
                    ),
                    rx.select(
                        DocumentosState.secciones,
                        placeholder="Sección",
                        value=DocumentosState.seccion,
                        on_change=DocumentosState.set_seccion,
                    ),
                    rx.select(
                        DocumentosState.estados,    
                        placeholder="Estado",
                        value=DocumentosState.estado,
                        on_change=DocumentosState.set_estado,
                    ),
                    rx.button(
                        "Buscar",
                        on_click=DocumentosState.buscar,
                        color_scheme="blue",
                    ),
                    rx.button(
                        "Limpiar",
                        on_click=DocumentosState.limpiar_filtros,
                        variant="outline",
                    ),
                    spacing="3",
                    wrap="wrap",
                    justify="center",
                    width="100%",
                    margin_top="-40px",
                ),
                
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Título"),
                            rx.table.column_header_cell("Subtítulo"),
                            rx.table.column_header_cell("Descripción"),
                            rx.table.column_header_cell("Origen"),
                            rx.table.column_header_cell("Sección"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Archivo"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            DocumentosState.documentos,
                            fila_documento,
                        )
                    ),
                    width="100%",
                    padding="8px",
                ),
            ),
        )
    
    )