import os
import pdfplumber
import docx  # `python-docx` when installing from conda
import openpyxl
import markdown2

# choose whichever file handling library you want for a particular filetype
# import it above then define a handler function below

# handler functions
def extract_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return markdown2.markdown(file.read())

def extract_pdf(file_path):
    with pdfplumber.open(file_path) as file:
        return "\n".join(page.extract_text() for page in pdf.pages)

def extract_docx(file_path):
    file = docx.Document(file_path)
    return "\n".join([para.text for para in file.paragraphs])

def extract_xlsx(file_path):
    file = openpyxl.load_workbook(file_path)
    text = []
    for sheet in file.worksheets:
        for row in sheet.iter_rows():
            text.append(" ".join([str(cell.value) for cell in row if cell.value]))
    return "\n".join(text)


# Mapping table
# associate each supported file extension with a handler function
file_type_handlers = {
    ".txt": extract_text,
    ".md": extract_markdown,
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".xlsx": extract_xlsx
}


# Master function
def extract_content(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext in file_type_handlers:
        return file_type_handlers[ext](file_path)
    else:
        raise ValueError(f"No handler available for file type: {ext}")
