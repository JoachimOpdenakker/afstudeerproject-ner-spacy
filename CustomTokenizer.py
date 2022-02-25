import spacy
from spacy.util import registry, compile_suffix_regex

@registry.callbacks("customize_tokenizer")
def make_customize_tokenizer():
    def customize_tokenizer(nlp):
        print("Ik heb een rode patat")
        infixes = nlp.Defaults.infixes + [r'\,']
        nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
    return customize_tokenizer