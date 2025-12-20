import reflex as rx
from portal.components.layout import layout
from portal.state.documento_state import DocumentoState


@rx.page(route="/subir-documento")
def subir_documento() -> rx.Component:
    return layout(
        rx.form(
            rx.vstack(
                rx.input(
                    name="titulo",
                    placeholder="Título",
                    required=True,
                ),

                rx.input(
                    type="file",
                    name="archivo",
                    accept=".pdf,.doc,.docx,.xls,.xlsx",
                    required=True,
                    size="2",
                ),


                rx.button("Guardar", type="submit"),
                spacing="3",
                width="100%",
                max_width="400px",
            ),
            on_submit=DocumentoState.submit,
            enc_type="multipart/form-data",
        )
    )













