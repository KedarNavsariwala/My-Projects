import os
import PyPDF2
from typing import List

class PDFProcessor:
    def __init__(self, pdf_dir: str, output_dir: str):
        self.pdf_dir = pdf_dir
        self.output_dir = output_dir

    def convert_pdf_to_text(self, pdf_path: str) -> str:
        """Convert a single PDF file to text."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return ""

    def process_all_pdfs(self) -> List[str]:
        """Process all PDFs in the directory and save as text files."""
        processed_files = []
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for filename in os.listdir(self.pdf_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_dir, filename)
                text = self.convert_pdf_to_text(pdf_path)
                
                if text:
                    # Save the text to a file
                    text_filename = os.path.splitext(filename)[0] + '.txt'
                    text_path = os.path.join(self.output_dir, text_filename)
                    
                    with open(text_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    
                    processed_files.append(text_path)
                    print(f"Processed: {filename}")

        return processed_files

    def clean_text(self, text: str) -> str:
        """Clean the extracted text."""
        # Remove multiple newlines
        text = ' '.join(text.split())
        # Remove special characters
        text = ''.join(char for char in text if char.isalnum() or char.isspace() or char in '.,!?-')
        return text.strip()
