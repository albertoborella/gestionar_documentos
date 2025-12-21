from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from enum import Enum

# ENUMS
class OrigenDocumento(str, Enum):
    interno = "interno"
    externo = "externo"

class SeccionDocumento(str, Enum):
    administracion = "administracion"
    produccion = "produccion"
    exportacion = "exportacion"
    servicios = "servicios"
    depositos = "depositos"

class TipoDocumento(str, Enum):
    procedimiento = "procedimiento"
    instructivo = "instructivo"
    legal = "legal"
    registro = "registro"

class EstadoDocumento(str, Enum):
    borrador = "borrador"
    en_aprobacion = "en_aprobacion"
    vigente = "vigente"
    obsoleto = "obsoleto"

# MODELOS
class DocumentoBase(SQLModel):
    titulo: str
    subtitulo: str | None = None
    descripcion: str | None = None
    origen: OrigenDocumento
    seccion: SeccionDocumento
    tipo: TipoDocumento
    estado: EstadoDocumento


class Documento(DocumentoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # 📄 INFO DEL ARCHIVO
    nombre_original: str
    extension: str
    mime_type: str
    tamanio: int
    ruta: str

    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DocumentoCrear(DocumentoBase):
    pass


class DocumentoModificar(DocumentoBase):
    titulo: str
    subtitulo: str | None = None
    descripcion: str | None = None
    origen: OrigenDocumento
    seccion: SeccionDocumento
    tipo: TipoDocumento
    estado: EstadoDocumento
    

    
    