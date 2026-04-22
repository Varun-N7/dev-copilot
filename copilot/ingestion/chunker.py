from langchain.text_splitter import RecursiveCharacterTextSplitter

LANGUAGE_SEPARATORS = {
    "py": ["\nclass ", "\ndef ", "\n\n", "\n", " ", ""],
    "js": ["\nfunction ", "\nconst ", "\n\n", "\n", " ", ""],
    "ts": ["\nfunction ", "\nconst ", "\nclass ", "\n\n", "\n", " ", ""],
}

def chunk_file(file: dict, chunk_size: int = 1000, overlap: int = 150) -> list[dict]:
    separators = LANGUAGE_SEPARATORS.get(file["language"], ["\n\n", "\n", " ", ""])
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=separators,
    )
    chunks = splitter.split_text(file["content"])
    return [
        {"text": chunk, "filepath": file["filepath"], "language": file["language"], "chunk_index": i}
        for i, chunk in enumerate(chunks)
    ]

def chunk_all_files(files: list[dict]) -> list[dict]:
    result = []
    for f in files:
        result.extend(chunk_file(f))
    return result
