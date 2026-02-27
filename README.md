
---

## Requisitos del sistema (Ubuntu)

```bash
sudo apt install tesseract-ocr tesseract-ocr-spa poppler-utils
```

Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```


Instalar
```bash
pip install -r requirements.txt
```



Ejemplo de uso
```python
from pdf_ocr_finder.search import search_in_pdf

resultado = search_in_pdf(
    pdf_path="documento.pdf",
    pattern=r"16\s*%"
)
```





