from pypdf import PdfReader


def extract_text(file):
    text = ""

    if file.filename.endswith(".pdf"):
        pdf = PdfReader(file.file)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    elif file.filename.endswith(".txt"):
        text = file.file.read().decode("utf-8")

    else:
        raise ValueError("Only PDF and TXT supported")

    return text.strip()


def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]

        if chunk:
            chunks.append(" ".join(chunk))

        start += chunk_size - overlap

    return chunks





