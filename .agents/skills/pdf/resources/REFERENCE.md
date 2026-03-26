# PDF Advanced Reference

## pypdfium2 - Advanced PDF Rendering

```python
import pypdfium2 as pdfium

# Open PDF
pdf = pdfium.PdfDocument("document.pdf")
print(f"Pages: {len(pdf)}")

# Render page as image
page = pdf[0]
bitmap = page.render(scale=2)  # 2x resolution
pil_image = bitmap.to_pil()
pil_image.save("page_1.png")
```

## JavaScript - pdf-lib

```javascript
import { PDFDocument } from 'pdf-lib';
import fs from 'fs';

// Read existing PDF
const existingPdfBytes = fs.readFileSync('input.pdf');
const pdfDoc = await PDFDocument.load(existingPdfBytes);

// Get pages
const pages = pdfDoc.getPages();
const firstPage = pages[0];

// Add text
firstPage.drawText('Hello World!', { x: 50, y: 500, size: 30 });

// Save
const pdfBytes = await pdfDoc.save();
fs.writeFileSync('output.pdf', pdfBytes);
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|:---|:---|
| Unicode characters not rendering | Use ReportLab XML tags (`<sub>`, `<super>`) instead of Unicode |
| Tables not extracting correctly | Try `pdfplumber` with custom table settings |
| Scanned PDF (no text layer) | Use OCR via `pytesseract` + `pdf2image` |
| Large PDF performance | Process pages lazily with generators |
| Password-protected PDF | Use `qpdf --decrypt` or `PdfReader(file, password=pwd)` |

### Installation Guide

```bash
# Core libraries
pip install pypdf pdfplumber reportlab

# OCR support
pip install pytesseract pdf2image
# Also requires Tesseract OCR engine and Poppler installed on system

# Advanced rendering
pip install pypdfium2

# CLI tools (Windows via chocolatey)
choco install poppler qpdf

# CLI tools (macOS via homebrew)
brew install poppler qpdf
```
