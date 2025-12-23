from pydantic import BaseModel
import reflex as rx
import httpx


class Documento(BaseModel):
    titulo: str
    subtitulo: str
    descripcion: str
    origen: str
    seccion: str
    estado: str
    ruta: str


class DocumentosState(rx.State):
    documentos: list[Documento] = []
    loading: bool = False
    error: str = ""

    async def cargar_documentos(self):
        self.loading = True
        self.error = ""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://127.0.0.1:8001/documentos/"
                )
                response.raise_for_status()

                self.documentos = [
                    Documento(
                        titulo=d["titulo"],
                        subtitulo=d["subtitulo"],
                        descripcion=d["descripcion"],
                        origen=d["origen"],
                        seccion=d["seccion"],
                        estado=d["estado"],
                        ruta=d["ruta"],
                    )
                    for d in response.json()
                ]

        except Exception as e:
            self.error = str(e)

        finally:
            self.loading = False








































        
        
