import reflex as rx
import httpx


class DocumentoState(rx.State):

    async def submit(self, form_data: dict):
        print("🔥 SUBMIT EJECUTADO")

        archivo_bytes = form_data.get("archivo")

        if not archivo_bytes:
            return rx.toast.error("Debe seleccionar un archivo")

        files = {
            "archivo": (
                "documento.pdf",
                archivo_bytes,
                "application/pdf",
            )
        }

        data = {
            "titulo": form_data.get("titulo"),
            "origen": "interno",
            "seccion": "administracion",
            "tipo": "procedimiento",
            "estado": "vigente",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8001/documentos/upload/",
                data=data,
                files=files,
                timeout=60,
            )

        if response.status_code == 200:
            return rx.toast.success("Documento cargado correctamente")
        else:
            print("❌ Error backend:", response.text)
            return rx.toast.error("Error al cargar documento")













        
        
