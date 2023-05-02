import json
import re

import pymorphy2
from razdel import tokenize, sentenize

morph = pymorphy2.MorphAnalyzer()
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsNERTagger,

    Doc
)
from collections import Counter


# Текст
with open('ТЗ - короткое.txt', 'r', encoding='utf-8-sig') as file:
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
for sent in sents:
    tokens = list(tokenize(text))
# print(tokens)

# POS-taggingл
pos_list = []
for i in tokens:
    pos_list.append([i.text, str(morph.parse(i.text)[0].tag)[:4]])
print(pos_list)

for pair in pos_list:
    for word, tag in ner_dict.items():
        if pair[0] == word:
            pair[1] = tag

with open('POS_tagging.json', 'w', encoding='utf-8-sig') as file:
    json.dump(pos_list, file, indent=4, ensure_ascii=False)


# выводим пос-тэггинг по парам
with open("POS_tagging.json", "r", encoding='utf-8-sig') as read_file:
    data = json.load(read_file)

ex_tags = ['PNCT']
tags = []
for i in range(len(data)-1):
    if data[i][1] in ex_tags or data[i+1][1] in ex_tags:
        pass
    else:
        # print(data[i], data[i+1])
        new_str = str(data[i][1] + ' ' + data[i+1][1])
        tags.append(new_str)
c = Counter(tags)

