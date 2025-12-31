from pydantic import BaseModel
from typing import Optional
import reflex as rx
import httpx


# ======================
# MODELO DOCUMENTO
# ======================
class Documento(BaseModel):
    id: int
    titulo: str
    subtitulo: str
    descripcion: str
    origen: str
    seccion: str
    estado: str
    ruta: str


# ======================
# STATE LISTADO
# ======================
class DocumentosState(rx.State):
    documentos: list[Documento] = []

    # paginado
    page: int = 1
    page_size: int = 10
    total_pages: int = 1

    # UI
    loading: bool = False
    error: str = ""

    # filtros
    texto: str = ""
    origen: str = ""
    seccion: str = ""
    estado: str = ""

    # enums
    origenes: list[str] = []
    secciones: list[str] = []
    estados: list[str] = []

    # -------- setters --------
    def set_texto(self, value: str):
        self.texto = value

    def set_origen(self, value: str):
        self.origen = value

    def set_seccion(self, value: str):
        self.seccion = value

    def set_estado(self, value: str):
        self.estado = value

    # -------- enums --------
    async def cargar_enums(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "http://127.0.0.1:8001/documentos/enums"
                )
                resp.raise_for_status()
                data = resp.json()

            self.origenes = data.get("origen", [])
            self.secciones = data.get("seccion", [])
            self.estados = data.get("estado", [])

        except Exception as e:
            self.error = f"Error cargando enums: {e}"

    # -------- core paginado --------
    async def cargar_documentos(self):
        self.loading = True
        self.error = ""

        params = {
            "page": self.page,
            "page_size": self.page_size,
        }

        # filtros
        if self.texto:
            params["texto"] = self.texto
        if self.origen:
            params["origen"] = self.origen
        if self.seccion:
            params["seccion"] = self.seccion
        if self.estado:
            params["estado"] = self.estado

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "http://127.0.0.1:8001/documentos/buscar",
                    params=params,
                )
                resp.raise_for_status()
                data = resp.json()

            self.documentos = [Documento(**d) for d in data]
            self.total_pages = max(1, (len(self.documentos) + self.page_size - 1) // self.page_size)

        except Exception as e:
            self.error = str(e)

        finally:
            self.loading = False

    # -------- acciones UI --------
    async def buscar(self):
        self.page = 1
        await self.cargar_documentos()

    def limpiar_filtros(self):
        self.texto = ""
        self.origen = ""
        self.seccion = ""
        self.estado = ""
        self.page = 1
        return DocumentosState.cargar_documentos

    async def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            await self.cargar_documentos()

    async def prev_page(self):
        if self.page > 1:
            self.page -= 1
            await self.cargar_documentos()

    # -------- urls --------
    @staticmethod
    def url_ver_documento(documento_id: int) -> str:
        return f"http://127.0.0.1:8001/documentos/{documento_id}/ver"

    @staticmethod
    def url_editar_documento(documento_id: int) -> str:
        return f"/editar-documento/{documento_id}"


# ======================
# STATE EDICIÓN
# ======================
class DocumentoEditState(rx.State):
    doc_id: Optional[str] = None

    titulo: str = ""
    subtitulo: str = ""
    descripcion: str = ""
    origen: str = ""
    seccion: str = ""
    estado: str = ""

    origenes: list[str] = []
    secciones: list[str] = []
    estados: list[str] = []

    loading: bool = False
    error: str = ""

    # setters
    def set_titulo(self, value: str):
        self.titulo = value

    def set_subtitulo(self, value: str):
        self.subtitulo = value

    def set_descripcion(self, value: str):
        self.descripcion = value

    def set_origen(self, value: str):
        self.origen = value

    def set_seccion(self, value: str):
        self.seccion = value

    def set_estado(self, value: str):
        self.estado = value

    async def cargar_enums(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "http://127.0.0.1:8001/documentos/enums"
                )
                resp.raise_for_status()
                data = resp.json()

            self.origenes = data.get("origen", [])
            self.secciones = data.get("seccion", [])
            self.estados = data.get("estado", [])

        except Exception as e:
            self.error = f"Error cargando enums: {e}"

    async def cargar_documento(self):
        self.loading = True
        self.error = ""

        self.doc_id = self.router.page.params.get("id")

        if not self.doc_id:
            self.error = "ID de documento no encontrado"
            self.loading = False
            return

        try:
            await self.cargar_enums()

            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"http://127.0.0.1:8001/documentos/{self.doc_id}"
                )
                resp.raise_for_status()
                data = resp.json()

            self.titulo = data.get("titulo", "")
            self.subtitulo = data.get("subtitulo", "")
            self.descripcion = data.get("descripcion", "")
            self.origen = data.get("origen", "")
            self.seccion = data.get("seccion", "")
            self.estado = data.get("estado", "")

        except Exception as e:
            self.error = str(e)

        finally:
            self.loading = False

    async def guardar_cambios(self):
        if not self.doc_id:
            self.error = "ID inválido"
            return

        self.loading = True
        self.error = ""

        try:
            payload = {
                "titulo": self.titulo,
                "subtitulo": self.subtitulo,
                "descripcion": self.descripcion,
                "origen": self.origen,
                "seccion": self.seccion,
                "estado": self.estado,
            }

            async with httpx.AsyncClient() as client:
                resp = await client.patch(
                    f"http://127.0.0.1:8001/documentos/{self.doc_id}",
                    json=payload,
                )
                resp.raise_for_status()

            return rx.redirect("/listar-documentos")

        except Exception as e:
            self.error = str(e)

        finally:
            self.loading = False








































        
        
