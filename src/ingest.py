import pymupdf #PyMuPDF
from pathlib import Path

DATA_DIR = Path("D:/Demo Projects/rag-contract-assistant/data/raw/cuad_dataset/CUAD_v1/full_contract_pdf")

def list_contract_pdfs(data_dir: Path)-> list[Path]:
    """Recursively find every contract PDF under the CUAD directory."""
    return sorted(data_dir.rglob("*.pdf")) 

def extract_text_from_pdf(pdf_path: Path) ->str:
    """Extract raw text from a single PDF, page by page."""
    doc = pymupdf.open(pdf_path)
    text=""
    for page in doc:
        text+=page.get_text()
    doc.close()
    return text

def audit_corpus(pdfs: list[Path])-> None:
    """Extract text from every pdfs & flag anything suspicious"""
    lengths=[]
    empty_or_short=[]

    for pdf_path in pdfs:
        text = extract_text_from_pdf(pdf_path)
        char_count=len(text.strip())
        lengths.append(char_count)

        if char_count<500:
            empty_or_short.append((pdf_path.name,char_count))

    print(f"\n Total PDFs: {len(lengths)}")
    print(f"Min Length: {min(lengths)}")
    print(f"max Length: {max(lengths)}")
    print(f"Avg length: {sum(lengths)/len(lengths):0.0f} chars")

    print(f"\nSuspiciously short/empty ({len(empty_or_short)}): ")
    for name, count in empty_or_short:
        print(f"{name}:{count} chars")

if __name__ == "__main__":

    print(DATA_DIR.exists())
    
    pdfs=list_contract_pdfs(DATA_DIR)
    print(f"Found {len(pdfs)} contract PDFs")

    audit_corpus(pdfs)
    # sample_path = pdfs[0]
    # print(f"\nInspecting: {sample_path.name}\n{'-' * 60}")

    # text = extract_text_from_pdf(sample_path)
    # print(text[:2000])
