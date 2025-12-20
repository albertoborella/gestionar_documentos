from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import select
from pathlib import Path
from datetime import datetime, timezone
from database import DocumentSession
from models import (Documento, 
                    OrigenDocumento,
                    SeccionDocumento,
                    TipoDocumento,
                    EstadoDocumento,)


from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
from datetime import datetime, timezone
import re

router = APIRouter(
    prefix="/documentos",
    tags=["documentos"],
)

DOCUMENTOS_DIR = Path("documentos")


def limpiar_nombre(texto: str) -> str:
    """Elimina caracteres raros y espacios del nombre"""
    texto = texto.strip().lower()
    texto = re.sub(r"[^\w\-]+", "_", texto)
    return texto


@router.post("/upload/", response_model=Documento)
async def crear_documento(
    titulo: str = Form(...),
    subtitulo: str | None = Form(None),
    descripcion: str | None = Form(None),
    origen: OrigenDocumento = Form(...),
    seccion: SeccionDocumento = Form(...),
    tipo: TipoDocumento = Form(...),
    estado: EstadoDocumento = Form(...),
    archivo: UploadFile = File(...),
    session: DocumentSession = None,
):
    DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)

    if not archivo or not archivo.filename:
        raise HTTPException(
            status_code=400,
            detail="No se proporcionó un archivo válido."
        )

    # 🔹 Extensión real del archivo
    extension = Path(archivo.filename).suffix.lower()

    if not extension:
        raise HTTPException(
            status_code=400,
            detail="El archivo no tiene extensión."
        )

    # 🔹 Nombre seguro
    titulo_limpio = limpiar_nombre(titulo)
    nombre_archivo = f"{titulo_limpio}{extension}"

    ruta = DOCUMENTOS_DIR / nombre_archivo

    # 🔹 Guardar archivo
    contenido = await archivo.read()
    with open(ruta, "wb") as f:
        f.write(contenido)

    documento = Documento(
        titulo=titulo,
        subtitulo=subtitulo,
        descripcion=descripcion,
        origen=origen,
        seccion=seccion,
        tipo=tipo,
        estado=estado,
        nombre_original=archivo.filename,
        nombre_archivo=nombre_archivo,
        extension=extension,
        mime_type=archivo.content_type or "application/octet-stream",
        tamanio=len(contenido),
        ruta=str(ruta),
        fecha_creacion=datetime.now(timezone.utc),
        fecha_actualizacion=datetime.now(timezone.utc),
    )

    session.add(documento)
    session.commit()
    session.refresh(documento)

    return documento



@router.get("/{documento_id}/", response_model=Documento)
async def obtener_documento(documento_id: int, session: DocumentSession = None):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    return documento


@router.get("/{documento_id}/ver")
async def ver_documento(documento_id: int, session: DocumentSession = None):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    
    ruta = Path(documento.ruta)
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="Archivo del documento no encontrado.")
    
    return FileResponse(
        path=ruta, 
        media_type=documento.mime_type, 
        filename=documento.nombre_original,
        )

@router.get("/", response_model=list[Documento])
def listar_documentos(session: DocumentSession = None):
    statement = select(Documento)
    documentos = session.exec(statement).all()
    if not documentos:
        raise HTTPException(status_code=404, detail="No se encontraron documentos.")
    return documentos

