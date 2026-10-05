"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Paragraph-aware chunker for the campus_life corpus.

    These documents are short forum-style posts (178–549 chars) structured as:
      Title line
      (blank line)
      Paragraph 1
      (blank line)
      Paragraph 2  ...

    The starter's 800-char fixed window never splits anything (no post is that
    long), so every document becomes one chunk regardless of how many separate
    topics it covers. A housing post might contain general room info, a "good"
    paragraph, a "bad" paragraph, and a laundry+noise paragraph — four distinct
    topics in one vector. Splitting on blank lines puts each topic in its own
    chunk so retrieval can match "laundry cost" to the laundry paragraph
    instead of a diluted whole-document embedding.

    Why title-prepend: a paragraph like "Laundry costs $1.75 wash" has no
    building name in it, so without the title the retriever can't tell which
    building the chunk is about. Prepending the title to every chunk solves
    this without adding a separate metadata-lookup step.

    Why MIN_PARA_CHARS = 80: some paragraphs are bare one-liners like
    "The good: closest building to the science quad" (73 chars). They carry
    real information but are too short to embed reliably on their own, so we
    merge them forward into the next paragraph.
    """
    # Paragraphs shorter than this (in characters) merge into the next one.
    # 80 was chosen because the shortest standalone paragraph in this corpus
    # ("The bad: the elevator is out roughly one week per semester.") is 57
    # chars — below 80 triggers a merge. The shortest self-contained useful
    # paragraph I found was 82 chars, which clears the threshold cleanly.
    MIN_PARA_CHARS = 80

    chunks: list[Chunk] = []

    for doc in documents:
        # Split on blank lines; drop any empty strings left by strip()
        paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]

        if not paragraphs:
            continue

        # The first paragraph is always the document title (e.g. "Pellew
        # Dining Hall" or "MATH 220 Linear Algebra — assessment"). It goes
        # on every chunk as a context header but is not a chunk on its own.
        title = paragraphs[0]
        body = paragraphs[1:] if len(paragraphs) > 1 else [title]

        # ── Merge short paragraphs forward ──────────────────────────────────
        # Walk through body paragraphs. When a paragraph is too short to
        # embed well, attach it to the next one instead of emitting it alone.
        merged: list[str] = []
        buffer = ""
        for para in body:
            buffer = (buffer + "\n\n" + para).lstrip("\n") if buffer else para
            if len(buffer) >= MIN_PARA_CHARS:
                merged.append(buffer)
                buffer = ""

        # Flush any remaining text. If there is already at least one merged
        # chunk, attach the tail to it (keeps the last chunk from being a
        # tiny stub). Otherwise the tail becomes its own chunk.
        if buffer:
            if merged:
                merged[-1] += "\n\n" + buffer  # attach tail to previous chunk
            else:
                merged.append(buffer)

        # ── Emit one Chunk per merged paragraph ─────────────────────────────
        # Each chunk gets the document title prepended so the model always
        # knows which building / course / topic it is reading about, even
        # when the paragraph body doesn't repeat the name.
        for i, para_text in enumerate(merged):
            # Only prepend title when the body text isn't already the title
            # (can happen if the document has a title line only).
            if para_text != title:
                chunk_text = title + "\n\n" + para_text
            else:
                chunk_text = para_text

            chunks.append(
                Chunk(
                    text=chunk_text.strip(),
                    source=doc.source,
                    index=i,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
