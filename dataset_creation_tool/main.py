import os
from pdf_processor import PDFProcessor
from llm_processor import LLMProcessor

def main():
    # Configure directories
    pdf_dir = r"C:\Users\kedar\OneDrive\Documents\GitHub\My-Projects\pdfs"
    text_dir = r"C:\Users\kedar\OneDrive\Documents\GitHub\My-Projects\output"
    json_dir = r"C:\Users\kedar\OneDrive\Documents\GitHub\My-Projects\final_output"

    # Initialize processors
    pdf_processor = PDFProcessor(pdf_dir, text_dir)
    llm_processor = LLMProcessor()

    # Ensure output directories exist
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    # Process PDFs
    processed_files = pdf_processor.process_all_pdfs()

    # Process each text file through LLM
    for text_path in processed_files:
        try:
            # Read the processed text
            with open(text_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # Clean the text
            cleaned_text = pdf_processor.clean_text(text)

            # Get grant ID from filename
            grant_id = os.path.splitext(os.path.basename(text_path))[0]

            # Process through LLM
            llm_output = llm_processor.process_text(cleaned_text)

            # Store results in JSON
            content = {
                "original_text": text,
                "cleaned_text": cleaned_text,
                "llm_analysis": llm_output
            }
            
            llm_processor.update_json_dataset(json_dir, grant_id, content)
            print(f"Successfully processed grant: {grant_id}")

        except Exception as e:
            print(f"Error processing {text_path}: {e}")

if __name__ == "__main__":
    main()
