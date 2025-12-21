import pymupdf4llm

def extract_pdf_to_markdown(pdf_path, output_path):
    """Extract text from PDF and save to markdown file using pymupdf4llm."""
    try:
        # Extract PDF content as markdown
        md_content = pymupdf4llm.to_markdown(pdf_path)
        
        # Write to markdown file
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(md_content)
        
        print(f"✓ Extracted content from {pdf_path}")
        print(f"✓ Saved to {output_path}")
        
    except Exception as e:
        print(f"✗ Error extracting {pdf_path}: {str(e)}")
        raise

if __name__ == "__main__":
    # Extract both DBT PDFs
    print("Extracting DBT-interview-plan.pdf...")
    extract_pdf_to_markdown(
        'DBT-interview-plan.pdf',
        'DBT-interview-plan-extracted.md'
    )
    
    print("\nExtracting DBT-example-plan.pdf...")
    extract_pdf_to_markdown(
        'DBT-example-plan.pdf',
        'DBT-example-plan-extracted.md'
    )
    
    print("\n✓ All PDFs extracted successfully!")
