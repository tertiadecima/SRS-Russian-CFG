from yargy import Parser, rule, or_
from yargy.predicates import gram, is_capitalized

# Define the grammar rules
NOUN = gram('NOUN')
PRONOUN = gram('NPRO')
VERB = gram('VERB')

# Define the parsing rule for a simple sentence
simple_sentence = rule(
    is_capitalized(),  # Subject starts with a capital letter
    or_(NOUN, PRONOUN),  # Subject can be a noun or a pronoun
    VERB  # Predicate is a verb
)

# Initialize the parser

ADJ = or_(gram('ADJF'), gram('ADJS'))
NOUN_MODIFIER = ADJ.repeatable()

# Update the parsing rule for a simple sentence
simple_sentence = rule(
    is_capitalized(),
    NOUN_MODIFIER.optional(),
    or_(NOUN, PRONOUN),
    VERB,
    NOUN.optional()  # Optional direct object
)

# Initialize the parser

PREP = gram('PREP')
PREP_PHRASE = rule(
    PREP,
    NOUN_MODIFIER.optional(),
    NOUN
)

# Update the parsing rule for a simple sentence
simple_sentence = rule(
    is_capitalized(),
    NOUN_MODIFIER.optional(),
    or_(NOUN, PRONOUN),
    VERB,
    NOUN.optional(),
    PREP_PHRASE.optional()  # Optional prepositional phrase
)

# Initialize the parser

CONJ = gram('CONJ')

# Define the parsing rule for a subordinate clause
subordinate_clause = rule(
    CONJ,
    simple_sentence
)

# Update the parsing rule for a simple sentence
simple_sentence = rule(
    is_capitalized(),
    NOUN_MODIFIER.optional(),
    or_(NOUN, PRONOUN),
    VERB,
    NOUN.optional(),
    PREP_PHRASE.optional(),
    subordinate_clause.optional()  # Optional subordinate clause
)

# Initialize the parser
parser = Parser(simple_sentence)

# Define the input sentences
with open('ТЗ - короткое.txt', 'r', encoding='utf-8-sig') as file:
    text = file.read()

for match in parser.findall(text):
    print([_.value for _ in match.tokens])

