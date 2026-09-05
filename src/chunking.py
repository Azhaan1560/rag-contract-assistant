from src.ingest import extract_text_from_pdf, list_contract_pdfs, DATA_DIR
from langchain_text_splitters import RecursiveCharacterTextSplitter


def fixed_size_chunk(text: str, chunk_size: int =1000, overlap: int=100)->list[str]:
    """Naively split text into fixed-size character windows with overlap."""
    chunks = []
    start=0
    while start<len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start+=chunk_size-overlap

    return chunks

def recursive_chunk(text: str, chunk_size: int =1000, overlap: int=100)->list[str]:
    """Split text respecting natural boundaries, falling back to smaller ones as needed."""
    splitter =RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)
if __name__ == "__main__":
    pdfs = list_contract_pdfs(DATA_DIR)
    sample_text = extract_text_from_pdf(pdfs[0])

    print(f"FIXED SIZE CHUNK:")
    chunks = fixed_size_chunk(sample_text)
    print(f"Document length: {len(sample_text)} chars")
    print(f"Number of chunks: {len(chunks)}")

    # Print a couple of chunk boundaries so you can see exactly where cuts happen
    for i in [0, 1, 2]:
        print(f"\n--- Chunk {i} (last 100 chars) ---")
        print(chunks[i][-100:])
        print(f"--- Chunk {i+1} (first 100 chars) ---")
        print(chunks[i+1][:100])

    print(f"LANGCHAIN SPLITTER CHUNKS")

    fixed = fixed_size_chunk(sample_text)
    recursive = recursive_chunk(sample_text)

    print(f"Document length: {len(sample_text)} chars")
    print(f"Fixed-size chunks:     {len(fixed)}")
    print(f"Recursive chunks:      {len(recursive)}")

    print("\n--- Recursive: boundary check (chunk 1 -> chunk 2) ---")
    print("End of chunk 1:", repr(recursive[1][-80:]))
    print("Start of chunk 2:", repr(recursive[2][:80]))
