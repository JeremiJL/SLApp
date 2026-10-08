from docxtpl import DocxTemplate

doc = DocxTemplate("templates/protocols/piuw.docx")
context = { 'NEXT_MONTH' : 8, 'MONTH' : 7, 'YEAR' : 2024}
doc.render(context)
doc.save("generated_doc.docx")
