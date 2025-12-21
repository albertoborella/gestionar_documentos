from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pathlib import Path
from datetime import datetime, timezone
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from database import get_session
from models import Documento, SeccionDocumento

router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"],
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
    origen="interno",              
    seccion="administracion",      
    tipo="registro",               
    estado="vigente",

    nombre_original=file.filename,
    nombre_archivo=file.filename,
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

# ===========================
# Obtener documento por ID
# ===========================
@router.get("/{documento_id}/", response_model=Documento)
async def obtener_documento(
    documento_id: int, 
    session: Session = Depends(get_session)
):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
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
# Listar todos los documentos
# ===========================
@router.get("/", response_model=list[Documento])
def listar_documentos(session: Session = Depends(get_session)):
    statement = select(Documento)
    documentos = session.exec(statement).all()
    if not documentos:
        raise HTTPException(status_code=404, detail="No se encontraron documentos")
    return documentos


