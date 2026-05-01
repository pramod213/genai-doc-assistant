
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from fastapi import HTTPException
import io


async def process_document(file):

    try:
        contents = await file.read()

        filename = file.filename.lower()

        text = ""

        # =========================
        # PDF Processing
        # =========================
        if filename.endswith(".pdf"):

            pdf_reader = PdfReader(io.BytesIO(contents))

            for page in pdf_reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text

        # =========================
        # TXT Processing
        # =========================
        elif filename.endswith(".txt"):

            text = contents.decode("utf-8")

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        # =========================
        # Chunking
        # =========================
        chunk_size = 500

        chunks = [
            {
                "text": text[i:i + chunk_size],
                "source": file.filename
            }
            for i in range(0, len(text), chunk_size)
        ]

        return chunks

    except PdfReadError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file"
        )

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="TXT file encoding must be UTF-8"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )