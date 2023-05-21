from yargy.predicates import gram
from yargy import Parser, rule, or_

# Define the grammar rules
from yargy.relations import gnc_relation

ADJ = gram('ADJF')
NOUN = gram('NOUN')
PREP = gram('PREP')

gnc = gnc_relation()

# Define the parsing rule
rule_sentence = rule(
    or_(
        rule(PREP, ADJ.optional().repeatable().match(gnc)),
        rule(ADJ.optional().repeatable())
    ),
    NOUN.repeatable().match(gnc),
    or_(
        rule(PREP, ADJ.optional().repeatable()),
        rule(ADJ.optional().repeatable())
    ),
    NOUN.optional().repeatable(),
)

# Define the input sentences
input_sentences = ["Создать единый визуальный каркас",
                   "Заложить основы идентификации городов",
                   "Реализовать пространство для баннеров по макету"]

TEST = rule(
    gram('INFN'),
    rule_sentence
)

# Initialize the parser
parser = Parser(TEST)

# Extract the output results
output_results = []
for sentence in input_sentences:
    matches = parser.findall(sentence)
    for match in matches:
        print([_.value for _ in match.tokens])
