from yargy.pipelines import morph_pipeline
from yargy.tokenizer import (
    Tokenizer,
    MorphTokenizer,
    EOL,
    EMAIL_RULE,
    PHONE_RULE
)

TOKENIZER = MorphTokenizer().remove_types(EOL).add_rules(EMAIL_RULE, PHONE_RULE)


class IdTokenizer(Tokenizer):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    # Используется при инициализации morph_pipeline, caseless_pipeline.
    # Строки-аргументы pipeline нужно разделить на слова. Как разделить,
    # например, "кейс| |dvd-диска" или "кейс| |dvd|-|диска"? Используем стандартный токенизатор.
    def split(self, text):
        return self.tokenizer.split(text)

    # Используется при инициализации предикатов. Например, есть предикат type('INT').
    # Поддерживает ли токенизатор тип INT?
    def check_type(self, type):
        return self.tokenizer.check_type(type)

    @property
    def morph(self):
        return self.tokenizer.morph

    def __call__(self, tokens):
        return tokens


ID_TOKENIZER = IdTokenizer(TOKENIZER)
gram('PRCL').optional(),
