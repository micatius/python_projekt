

def chunk_text(text, max_words=400):
    words = text.split()
    chunks = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return chunks



def translate_text(filepath, source_language_code: str, target_language_code: str) -> str:
    from transformers import pipeline

    translator = pipeline(
        "translation",
        model="../../resources/for_text_summarisation/mbart-large-50-many-to-many-mmt",
        tokenizer="../../resources/for_text_summarisation/mbart-large-50-many-to-many-mmt"
    )

    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()


    try:
        chunks = chunk_text(text, max_words=400)
    except Exception as e:
        raise ValueError("Error while chunking text") from e

    translated_chunks = []
    for chunk in chunks:
        try:
            translated = translator(chunk, src_lang="en_XX", tgt_lang='hr_HR', max_length=400)[0]['translation_text']
            translated_chunks.append(translated)
        except Exception as e:
            raise ValueError(f"Translation failed for chunk: {chunk[:50]}...") from e

    translated_text = ' '.join(translated_chunks)

    return translated_text