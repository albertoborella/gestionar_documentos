from pydantic import BaseModel
from typing import Optional
import reflex as rx
import httpx


class Documento(BaseModel):
    id: int
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

    # Filtros
    texto: str = ""
    origen: str = ""
    seccion: str = ""
    estado: str = ""

    # Enums dinámicos
    origenes: list[str] = []
    secciones: list[str] = []
    estados: list[str] = []

    # ✅ setters explícitos (evitan warnings y futuro break)
    def set_texto(self, value: str):
        self.texto = value

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
                data = resp.json()
                self.origenes = data.get("origen", [])
                self.secciones = data.get("seccion", [])
                self.estados = data.get("estado", []) 

        except Exception as e:
            self.error = f"Error cargando enums: {e}"  


    async def buscar(self):
        self.loading = True
        self.error = ""

        params = {}
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
                response = await client.get(
                    "http://127.0.0.1:8001/documentos/buscar",
                    params=params,
                )
                response.raise_for_status()

                self.documentos = [
                    Documento(**d) for d in response.json()
                ]

        except Exception as e:
            self.error = str(e)

        finally:
            self.loading = False

    def limpiar_filtros(self):
        self.texto = ""
        self.origen = ""
        self.seccion = ""
        self.estado = ""
        return DocumentosState.buscar
    
    @staticmethod
    def url_ver_documento(documento_id: int) -> str:
        return f"http://127.0.0.1:8001/documentos/{documento_id}/ver"

    @staticmethod
    def url_editar_documento(documento_id: int) -> str:
        return f"/editar-documento/{documento_id}"
    

class DocumentoEditState(rx.State):
    # --- Identificador (DEBE ser Optional) ---
    doc_id: Optional[str] = None

    # --- Campos del documento ---
    titulo: str = ""
    subtitulo: str = ""
    descripcion: str = ""
    origen: str = ""
    seccion: str = ""
    estado: str = ""

    # --- Enums dinámicos ---
    origenes: list[str] = []
    secciones: list[str] = []
    estados: list[str] = []

    # --- Estado UI ---
    loading: bool = False
    error: str = ""

    # --- setters explícitos ---
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

    # --- cargar enums ---
    async def cargar_enums(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://127.0.0.1:8001/documentos/enums")
                resp.raise_for_status()
                data = resp.json()

            self.origenes = data.get("origen", [])
            self.secciones = data.get("seccion", [])
            self.estados = data.get("estado", [])

        except Exception as e:
            self.error = f"Error cargando enums: {e}"

    # --- cargar documento existente ---
    async def cargar_documento(self):
        self.loading = True
        self.error = ""

        # ⚠️ API vigente (aunque esté deprecada)
        self.doc_id = self.router.page.params.get("id")

        if not self.doc_id:
            self.error = "ID de documento no encontrado en la URL"
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

    # --- guardar cambios ---
    async def guardar_cambios(self):
        if not self.doc_id:
            self.error = "ID de documento no válido"
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







































        
        
