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
            rx.hstack(
                rx.link(
                    "Ver",
                    href=DocumentosState.url_ver_documento(doc.id),
                    is_external=True,
                ),
                rx.link(
                    "Editar",
                    href=f"/editar-documento/{doc.id}",
                ),
                spacing="3",
            )
        ),
    )




@rx.page(
    route="/listar-documentos",
    on_load=[
        DocumentosState.cargar_enums,
        DocumentosState.cargar_documentos,
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
                #rx.text("Listado de Documentos", font_size="2xl", font_weight="bold"),

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
                    margin_top="-30px",
                ),
                
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Título"),
                            rx.table.column_header_cell("Grupo"),
                            rx.table.column_header_cell("Descripción"),
                            rx.table.column_header_cell("Seccion"),
                            rx.table.column_header_cell("Origen"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Acciones"),
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
                rx.center(
                    rx.hstack(
                        rx.button(
                            "◀ Anterior",
                            on_click=DocumentosState.prev_page,
                            is_disabled=DocumentosState.page <= 1,
                            variant="outline",
                        ),

                        rx.text(
                            rx.hstack(
                                rx.text("Página "),
                                rx.text(DocumentosState.page, font_weight="bold"),
                                rx.text(" de "),
                                rx.text(DocumentosState.total_pages, font_weight="bold"),
                            )
                        ),

                        rx.button(
                            "Siguiente ▶",
                            on_click=DocumentosState.next_page,
                            is_disabled=DocumentosState.page >= DocumentosState.total_pages,
                            variant="outline",
                        ),

                        spacing="4",
                        align="center",
                    ),
                    width="100%",
                    margin_top="16px",
                )

            ),

        )
    )