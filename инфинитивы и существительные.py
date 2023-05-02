from yargy.predicates import eq
from yargy import Parser, rule, and_, or_, not_
from yargy.predicates import gram, dictionary, in_

# CONDITION = rule(
#     dictionary({'При'}),
#     gram('NOUN'),
#     or_(
#         gram('CONJ'),
#         gram('PNCT')
#     ).optional(),
#     gram('NOUN').optional().repeatable(max=2)
# )

NO = in_(['не', 'нет', 'ни'])

ADJ_FOR_NOUN = rule(
    NO.optional(),

    or_(
        gram('ADJF'),
        gram('PRTF'),
    ),
)

ADVB = rule(
    NO.optional(),

    gram('ADVB'),
)

N_NP = rule(
    NO.optional(),

    or_(
        rule(
            ADJ_FOR_NOUN.optional().repeatable(),
            gram('NOUN'),
        ),
        rule(
            ADJ_FOR_NOUN.optional().repeatable(),
            gram('NOUN'),
            ADJ_FOR_NOUN.optional(),
            gram('NOUN').repeatable()
        )
    )
)

PREP_NOUN = rule(
    gram('PREP'),

    N_NP,

    rule(
        gram('CONJ'),
        N_NP
    ).optional()
)

ANY_VERB = rule(
    NO.optional(),

    or_(
        gram('VERB'),
        gram('INFN'),
    ),
)

DIRECT = rule(
    or_(  # прямые дополнения для /что-то/ (выше)
        rule(
            ADJ_FOR_NOUN.optional().repeatable(),
            gram('NOUN').optional(),
        ),
        rule(
            gram('NOUN').repeatable(),
        ),
        rule(
            gram('INFN'),
            ADJ_FOR_NOUN.optional().repeatable(),
            gram('NOUN').repeatable(),
        )
    ),
)


def bounded(start, stop):
    return rule(
        eq(start),
        not_(eq(stop)).repeatable(),
        eq(stop)
    )


BOUNDED = or_(
    bounded('[', ']'),
    bounded('«', '»')
)

PARENTHESES = rule(bounded('(', ')'))

# -------------------------------------------------------------------------------------------------------------

INF_NOUN = rule(
    #  кнопку переключения,

    or_(  # прямое и непрямое дополнение в начале предложения
        PREP_NOUN.optional().repeatable(),
        N_NP.optional(),
    ),

    gram('PRCL').optional(),
    NO.optional(),

    rule(  # ['надо', 'надо будет', 'нужно', 'нужно будет', 'обязательно', 'должно']
        gram('PRED'),
        dictionary(['будет']).optional()
    ).optional(),
    gram('PRCL').optional(),

    gram('INFN'),

    gram('PREP').optional(),
    NO.optional(),

    N_NP.optional(),

    NO.optional(),

    DIRECT,

    PREP_NOUN.optional().repeatable(),  # непрямое дополнение в конце предложения

)

# -------------------------------------------------------------------------------------------------------------

CONJ = in_(['что', 'чтобы', 'что бы'])

INF_SO_THAT = rule(  # для блока "делать так, что/чтобы", "надо, чтобы"

    CONJ,

    gram('PREP').optional(),
    ADJ_FOR_NOUN.optional().repeatable(),
    N_NP,  # зачем мне этот кусок?

    PREP_NOUN.optional().repeatable(),

    ADVB.optional(),

    ANY_VERB.optional(),

    N_NP.optional(),

    DIRECT,

)

# -------------------------------------------------------------------------------------------------------------

VERB_US = rule(

    dictionary(['мы']).optional(),

    DIRECT.optional(),

    NO.optional(),
    and_(
        gram('VERB'),
        gram('plur'),
        gram('1per')
    ),

    INF_NOUN.optional(),

    DIRECT.optional(),

)

# -------------------------------------------------------------------------------------------------------------

SECOND_PART = rule(  # сочинительная часть после запятой
    in_(['и', 'но', 'а']),
    or_(
        INF_NOUN,
        INF_SO_THAT
    )
)

IF = rule(  # подчинительная-условная часть после запятой

)

# -------------------------------------------------------------------------------------------------------------

with open('ТЗ - короткое.txt', 'r', encoding='utf-8-sig') as file:
    text = file.read()
parser = Parser(VERB_US)

for match in parser.findall(text):
    print([_.value for _ in match.tokens])
