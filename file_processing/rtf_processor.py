from file_processor_strategy import FileProcessorStrategy
from striprtf.striprtf import rtf_to_text
#https://pypi.org/project/striprtf/
import fpdf as FPDF

class RtfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        self.metadata.update({"text": rtf_to_text(file_content)})

    def save(self, output_path: str = None) -> None:
        save_path = output_path or self.file_path
        with open(save_path, 'w') as f:
            f.write(self.metadata['text'])
    
    def save_as_pdf(self, output_path: str) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size = 12)
        
        with open(self.file_path, "r") as f:
            for x in f:
                x = x.encode('utf-8').decode('latin1')
                pdf.multi_cell(200,10, txt = x.strip(), align = 'C')
        pdf.output(output_path)
    
    def save_as_docx(self, output_path: str) -> None:
        from docx import Document
        docx_file = Document()
        with open(self.file_path, 'r') as f:
            text = f.read()
            docx_file.add_paragraph(text)

        docx_file.save(output_path)