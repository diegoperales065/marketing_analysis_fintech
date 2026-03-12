# PDF Forms - Filling and Processing

## Reading Form Fields

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
fields = reader.get_fields()

# List all form fields
for field_name, field_data in fields.items():
    print(f"Field: {field_name}")
    print(f"  Type: {field_data.get('/FT', 'Unknown')}")
    print(f"  Value: {field_data.get('/V', 'Empty')}")
    print()
```

## Filling Form Fields

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()

# Clone the PDF
writer.append(reader)

# Fill fields
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "name_field": "John Doe",
        "email_field": "john@example.com",
        "date_field": "2024-01-15",
    }
)

# Save filled form
with open("filled_form.pdf", "wb") as output:
    writer.write(output)
```

## Flattening Forms (Make Fields Non-Editable)

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("filled_form.pdf")
writer = PdfWriter()
writer.append(reader)

# Flatten all form fields
for page in writer.pages:
    for annot in page.get("/Annots", []):
        annot.get_object().update({"/Ff": 1})

with open("flattened.pdf", "wb") as output:
    writer.write(output)
```

## Checkbox and Radio Button Fields

```python
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "checkbox_field": "/Yes",      # Check a checkbox
        "radio_field": "/Option1",     # Select a radio option
    }
)
```

## Tips

- Always inspect form fields first with `get_fields()` before filling
- Field names are case-sensitive
- Checkbox values are typically `/Yes` or `/Off`
- Radio buttons use the option value prefixed with `/`
- Some PDFs have flattened forms that cannot be filled programmatically — use OCR approach instead
