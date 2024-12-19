

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/mT5_m2m_crossSum_enhanced")
    model = AutoModelForSeq2SeqLM.from_pretrained("csebuetnlp/mT5_m2m_crossSum_enhanced")

    tokenizer.save_pretrained("../../resources/for_text_summarisation/csebuetnlp/mT5_m2m_crossSum_enhanced")

    model.save_pretrained("../../resources/for_text_summarisation/csebuetnlp/mT5_m2m_crossSum_enhanced")