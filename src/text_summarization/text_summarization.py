
def chunk_text(text, max_words=500):
    words = text.split()
    chunks = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return chunks


def summarize_text(filepath) -> str:
    from transformers import pipeline

    summarizer = pipeline("summarization", model="../../resources/for_text_summarisation/facebook/bart-large-cnn")
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()

    chunks = chunk_text(text, 500)
    for chunk in chunks:
        print(chunk)
    summarized_chunks = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length=300, min_length=30, do_sample=False)[0]['summary_text']
        summarized_chunks.append(summary)

    summarized_text = ' '.join(summarized_chunks)

    return summarized_text
