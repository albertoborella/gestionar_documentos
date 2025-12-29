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







































        
        
