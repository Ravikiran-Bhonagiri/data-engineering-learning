import pymupdf4llm
import os

pdf_dir = r'd:\Ravikiran-Bhonagiri\data-engineering-portfolio\airflow'
output_dir = pdf_dir

pdfs = [
    'airflow-plan.pdf',
    'airflow-basics.pdf', 
    'airflow-examples.pdf'
]

for pdf_file in pdfs:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    output_file = pdf_file.replace('.pdf', '-extracted.md')
    output_path = os.path.join(output_dir, output_file)
    
    try:
        # Extract to markdown format
        md_text = pymupdf4llm.to_markdown(pdf_path)
        
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(f"# Extracted from {pdf_file}\n\n")
            output.write(md_text)
        
        print(f"✓ Extracted: {pdf_file} -> {output_file}")
    
    except Exception as e:
        print(f"✗ Error extracting {pdf_file}: {str(e)}")

print("\nExtraction complete!")
