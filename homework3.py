queries, sentences = [], []

def getInputs(queries_list, sentences_list, filename):
    with open(filename, 'r') as input_file:
        lines = input_file.readlines()
    no_of_queries = int(lines[0])
    no_of_sentences = int(lines[no_of_queries + 1])
    for query in range(1, no_of_queries + 1):
        queries_list.append(lines[query].strip('\n'))
    for sentence in range(no_of_queries + 2, no_of_queries + 2 + no_of_sentences):
        sentences_list.append(lines[sentence].strip('\n'))
    pass

def is_single_literal(sentence):
    if len(sentence.split('|')) == 1:
        return True
    else:
        return False

def resolveIfLiteralPresent(query):
    predicate = query.split('(')[0]
    for sentence in sentences:
        if is_single_literal(sentence) and predicate in sentence:
            return True
    return False

def resolve(query):
    return resolveIfLiteralPresent(query) or resolveByImplication(query) or resolveByOrElimination(query)

def findImplicationSentencesInWhichQueryExists(query):
    implicationSentences = []
    for sentence in sentences:
        if len(sentence.split('|')) == 2 and query in sentence.split('|')[1]:
                implicationSentences.append(sentence)
    return implicationSentences

def negation(term):
    if '~' in term:
        term = term.strip('~')
    else:
        term = '~' + term
    return term


def getPredicate(query):
    return query.split('(')[0]

def findDNFInWhichQueryExists(query):
    for sentence in sentences:
        if getPredicate(query) in sentence:
            disjunct_list = sentence.split('|')
    disjunct_list = list(map(str.strip, disjunct_list))[:-1]
    neg_disjunct_list = list(map(negation, disjunct_list))
    return neg_disjunct_list

def resolveByOrElimination(query):
    neg_disjuncts = findDNFInWhichQueryExists(query) #TODO do for all such sentences
    for neg_disjunct in neg_disjuncts:
        if not resolve(neg_disjunct):
            return False
    return True

def get_premises(sentences):
    premises = []
    for sentence in sentences:
        premises.append(negation(sentence.split('|')[0]).strip())
    return premises

def resolveByImplication(query):
    premises = get_premises(findImplicationSentencesInWhichQueryExists(query))
    for premise in premises:
        if resolve(premise):
            return True
    return False

if __name__ == '__main__':
    getInputs(queries, sentences, 'input.txt')
    print(resolve('R(x)'))