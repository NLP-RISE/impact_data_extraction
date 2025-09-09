from spacy import language as spacy_language

from utils.log_utils import Logging

class SpacyUtils:
    def __init__(self):
        self.logger = Logging.get_logger("normalize-utils")

    def load_spacy_model(self, spacy_model: str = "en_core_web_trf") -> spacy_language.Language:
        import spacy

        try:
            nlp = spacy.load(spacy_model, enable=["transformer", "ner", "tagger"])
            self.logger.info(f"SpaCy model '{spacy_model}' has been loaded")

        except OSError:
            self.logger.info(
                f"SpaCy model '{spacy_model}' is not downloaded. Dowloading now - this might take a minute"
            )
            from spacy.cli import download

            download(spacy_model)
            nlp = spacy.load(spacy_model)
        return nlp
