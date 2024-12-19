# Load model directly
from transformers import AutoTokenizer, AutoModel, GenerationConfig

if __name__ == "__main__":
    # Load tokenizer and model (ensure the correct model name is provided)
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModel.from_pretrained("facebook/bart-large-cnn")

    # Save tokenizer and model locally
    tokenizer.save_pretrained("../../resources/for_text_summarisation/facebook/bart-large-cnn")
    model.save_pretrained("../../resources/for_text_summarisation/facebook/bart-large-cnn")

# C:\Users\micatius\.virtualenvs\python_projekt-main-vEaSlPdb\Lib\site-packages\transformers\configuration_utils.py:393: UserWarning: Some non-default generation parameters are set in the model config. These should go into either a) `model.generation_config` (as opposed to `model.config`); OR b) a GenerationConfig file (https://huggingface.co/docs/transformers/generation_strategies#save-a-custom-decoding-strategy-with-your-model).This warning will become an exception in the future.
# Non-default generation parameters: {'max_length': 142, 'min_length': 56, 'early_stopping': True, 'num_beams': 4, 'length_penalty': 2.0, 'no_repeat_ngram_size': 3, 'forced_bos_token_id': 0}
#   warnings.warn(