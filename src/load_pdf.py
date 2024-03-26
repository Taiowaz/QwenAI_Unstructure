import os

dir = "./file/Aluminium_pdf_report"

files = os.listdir(dir)
for file_name in files:
    file_path = os.path.join(dir, file_name)

    with open(file_path, 'r') as file:
        