import json
from collections import Counter
import nltk
from nltk.util import ngrams

with open('POS_tagging.json', 'r', encoding='utf-8-sig') as file:
    pos_sents = json.load(file)
    templates_pos = []
    count_sentences = Counter()
    count_bigrams = Counter()
    count_trigrams = Counter()
    for sentence in pos_sents:
        print(sentence)
        tags = []
        # tags = [tag.split(',')[0] for word, tag in sentence]
        for word, tag in sentence:
            pos_tag = tag.split(',')[0]
            tags.append(pos_tag)
        count_sentences[' '.join(tags)] += 1

        bigrm = list(nltk.bigrams(tags))
        for bi in bigrm:
            count_bigrams[bi] += 1

        trigrm = ngrams(tags, 3)
        for tri in trigrm:
            count_trigrams[tri] += 1

    print('Так, объясняю. Вместо слов я тут использую чисто частеречные теги. Надо будет - прикрутим слова к этим '
          'тегам. Сейчас главное понять, есть ли какая-то закономерность и нужно ли в эту сторону двигаться. \nВ '
          'результате я посчитала количество разных шаблонов предложений, а также количество разных шаблонов биграм и '
          'триграм.\nВывод о том, насколько это имеет смысл, надо делать вместе, я вообще не ебу, если честно')
    # print(count_sentences)
    for i in count_bigrams:
        print(i)
    # print(count_bigrams)
    # print(count_trigrams)
    for i in count_bigrams:
        print(i)

'''Тут я поняла, что все хуйня и пошла для начала ручками это размечать. Ща буду делать вручную шаблоны, заебало меня'''

"""Шаблоны в рот их еблоны
    как идея пока
    там структура предложений все время такая
    1. нужно/надо (сделать) x (при _условиях_) (где (в приложении))
    2. сделать x так же как y
    3. сделать x (при _условиях_)
    4. X (делает) y (при _условиях_) (в приложении)"""


rules = [('(нужно|надо)', '(VERB|INFN)'),
         ('(сделать|делать)', '(NOUN|NPRO)'),
         ('(сделать|делать)', '()')]
