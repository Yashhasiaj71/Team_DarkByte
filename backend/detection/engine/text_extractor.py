"""
Text extraction from uploaded files.

Supports:
- Plain text (.txt)
- PDF (.pdf) via PyPDF2
- Images (.jpg, .png, etc.) via EasyOCR

"""

import io
from PyPDF2 import PdfReader


def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Extract raw text from a file based on its extension.

    Args:
        file_bytes: Raw bytes of the file
        filename: Original filename (used to determine format)

    Returns:
        Extracted text as a string
    """
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        return _extract_pdf(file_bytes)
    elif any(lower_name.endswith(ext) for ext in {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".tif"}):
        return _extract_image(file_bytes)
    else:
        # Default: treat as plain text
        return _extract_text(file_bytes)


def _extract_text(file_bytes: bytes) -> str:
    """Extract text from a plain text file."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1", errors="replace")


def _extract_pdf(file_bytes: bytes) -> str:
    """Extract text from all pages of a PDF."""
    reader = PdfReader(io.BytesIO(file_bytes))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)
    return "\n".join(pages_text)


def _extract_image(file_bytes: bytes) -> str:
    """Extract text from an image using EasyOCR (supports handwriting)."""
    import easyocr
    import numpy as np
    import cv2
    import os
    from django.conf import settings

    # EasyOCR expects a file path, numpy array, or bytes
    # For bytes, we need to decode to an image array first for better handling
    try:
        nparr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Check for custom model
        # Try to load custom model 'custom.pth' from detection/engine/models/
        model_dir = os.path.join(settings.BASE_DIR, 'detection', 'engine', 'models')
        custom_model_path = os.path.join(model_dir, 'custom.pth')
        
        if os.path.exists(custom_model_path):
            print(f"Using custom OCR model: {custom_model_path}")
            # Initialize reader with custom model
            reader = easyocr.Reader(
                ['en'], 
                gpu=False,
                model_storage_directory=model_dir,
                user_network_directory=model_dir,
                recog_network='custom' # Corresponds to custom.pth
            )
        else:
            print("Using default EasyOCR model (English)")
            # Initialize reader (load default English model)
            # gpu=False ensures it runs on CPU if CUDA isn't available
            reader = easyocr.Reader(["en"], gpu=False)

        # detail=0 returns just the text list
        results = reader.readtext(img, detail=0, paragraph=True)
        return "\n".join(results)
    except Exception as e:
        # Fallback or error logging
        print(f"OCR Error: {e}")
        return ""
