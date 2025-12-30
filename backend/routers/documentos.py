from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from pathlib import Path
from datetime import datetime, timezone
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from sqlalchemy import or_

from database import get_session
from models import Documento, DocumentoModificar, EstadoDocumento, OrigenDocumento, SeccionDocumento, TipoDocumento



router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"],
)

# ===========================
# Listar por filtros
# ===========================
@router.get("/buscar", response_model=list[Documento])
def buscar_documentos(
    texto: str | None = Query(default=None),
    origen: OrigenDocumento | None = None,
    seccion: SeccionDocumento | None = None,
    estado: EstadoDocumento | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Documento)

    if texto:
        like = f"%{texto}%"
        statement = statement.where(
            or_(
                Documento.titulo.ilike(like),
                Documento.subtitulo.ilike(like),
                Documento.descripcion.ilike(like),
            )
        )

    if origen:
        statement = statement.where(Documento.origen == origen)

    if seccion:
        statement = statement.where(Documento.seccion == seccion)

    if estado:
        statement = statement.where(Documento.estado == estado)

    return session.exec(statement).all()

# ===========================
# Enums dinámicos
# ===========================
@router.get("/enums")
def obtener_enums():
    return {
        "origen": [e.value for e in OrigenDocumento],
        "seccion": [e.value for e in SeccionDocumento],
        "estado": [e.value for e in EstadoDocumento],
    }

# ===========================
# Listar todos los documentos
# ===========================
@router.get("/", response_model=list[Documento])
def listar_documentos(session: Session = Depends(get_session)):
    statement = select(Documento)
    documentos = session.exec(statement).all()
    if not documentos:
        raise HTTPException(status_code=404, detail="No se encontraron documentos")
    return documentos

# ===========================
# Obtener documento por ID
# ===========================
@router.get("/{documento_id}", response_model=Documento)
async def obtener_documento(
    documento_id: int, 
    session: Session = Depends(get_session)
):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento

# ===========================
# Modificar un documento
# ===========================
@router.put("/{documento_id}")
def modificar_documento(
    documento_id: int,
    datos: DocumentoModificar,
    session: Session = Depends(get_session),
):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(documento, campo, valor)

    documento.fecha_actualizacion = datetime.now(timezone.utc)

    session.add(documento)
    session.commit()
    session.refresh(documento)

    return documento

# ===========================
# Ver o descargar documento
# ===========================
@router.get("/{documento_id}/ver")
async def ver_documento(
    documento_id: int, 
    session: Session = Depends(get_session)
):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    ruta = Path(documento.ruta)
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo del documento no encontrado")

    return FileResponse(
        path=ruta,
        media_type=documento.mime_type,
        filename=documento.nombre_original,
    )

# ===========================
# Subir un documento
# ===========================

DOCUMENTOS_DIR = Path("documentos")
DOCUMENTOS_DIR.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_documento(
    file: UploadFile = File(...),   # 🔥 CLAVE ABSOLUTA
    session: Session = Depends(get_session),
):
    ruta = DOCUMENTOS_DIR / file.filename

    with open(ruta, "wb") as f:
        f.write(await file.read())

    ahora = datetime.now(timezone.utc)

    documento = Documento(
    titulo=file.filename,
    subtitulo="",
    descripcion="",

    origen=OrigenDocumento.interno,
    seccion=SeccionDocumento.administracion,  
    tipo=TipoDocumento.registro,               
    estado=EstadoDocumento.borrador,

    nombre_original=file.filename,
    extension=ruta.suffix,
    mime_type=file.content_type,   
    tamanio=ruta.stat().st_size,
    ruta=str(ruta),

    fecha_creacion=ahora,
    fecha_actualizacion=ahora,
)

    session.add(documento)
    session.commit()
    session.refresh(documento)

    return documento
