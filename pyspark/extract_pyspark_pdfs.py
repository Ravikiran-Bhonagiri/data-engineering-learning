# PySpark PDF Extraction Script
import pymupdf4llm
import os

# PDF files to extract
pdf_files = [
    "pyspark-plan.pdf",
    "pyspark-basics.pdf", 
    "pyspark-examples.pdf"
]

# Extract each PDF
for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        print(f"Extracting {pdf_file}...")
        md_text = pymupdf4llm.to_markdown(pdf_file)
        
        # Save as markdown
        output_file = pdf_file.replace('.pdf', '-extracted.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Extracted from {pdf_file}\n\n")
            f.write(md_text)
        
        print(f"  Saved to {output_file}")
    else:
        print(f"  File not found: {pdf_file}")

print("\nExtraction complete!")
