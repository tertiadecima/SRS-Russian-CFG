import json
import re
import pymorphy2
from razdel import tokenize, sentenize

from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsNERTagger,

    Doc
)

# TODO: добавить NamesExtractor в импорт из наташи, нам имена тоже нужны

morph = pymorphy2.MorphAnalyzer()


# Текст
# with open('ТЗ - короткое.txt', 'r', encoding='utf-8-sig') as file:
with open('ТЗ по внедрению городов в моб. приложение.txt', 'r', encoding='utf-8-sig') as file:
    text = file.read()
# print(text)

# Выделение ссылок, адресов, NE,
url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
text = re.sub(url_extract_pattern, '', text)

doc = Doc(text)
segmenter = Segmenter()
doc.segment(segmenter)
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)

doc.tag_ner(ner_tagger)
ner_dict = {}
for i in doc.spans:
    ner_dict[i.text] = i.type

# Токенизация текста

text_newline = text.split('\n')
sents = []
for part in text_newline:
    sents.append(list(sentenize(part))[0].text)

sents = list(sentenize(text))
# print(sents)

pos_list = []

for sent in sents:
    tokens = list(tokenize(sent.text))
    sentence = []
    for i in tokens:
        sentence.append([i.text, str(morph.parse(i.text)[0].tag)])
    pos_list.append(sentence)

# print(tokens)

# POS-tagging
print(pos_list)

for pair in pos_list:
    for word, tag in ner_dict.items():
        if pair[0] == word:
            pair[1] = tag

with open('POS_tagging.json', 'w', encoding='utf-8-sig') as file:
    json.dump(pos_list, file, indent=4, ensure_ascii=False)
