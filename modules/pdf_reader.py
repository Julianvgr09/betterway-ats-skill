import fitz  # pymupdf
import os

def read_pdfs_from_folder(folder_path: str) -> dict:
    """
    Lee todos los PDFs de una carpeta y retorna un diccionario
    con el nombre del archivo como clave y el texto extraído como valor.
    """
    results = {}
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Carpeta no encontrada: {folder_path}")
    
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        raise ValueError(f"No se encontraron PDFs en: {folder_path}")
    
    for filename in sorted(pdf_files):
        filepath = os.path.join(folder_path, filename)
        try:
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            results[filename] = text.strip()
            print(f"  ✓ Leído: {filename}")
        except Exception as e:
            print(f"  ✗ Error leyendo {filename}: {e}")
            results[filename] = ""
    
    return results