
queries, sentences = [], []

def getInputs():
    with open('input.txt', 'r') as input_file:
        lines = input_file.readlines()
    no_of_queries = int(lines[0])
    no_of_sentences = int(lines[no_of_queries + 1])
    for query in range(1, no_of_queries + 1):
        queries.append(lines[query].strip('\n'))
    for sentence in range(no_of_queries + 2, no_of_queries + 2 + no_of_sentences):
        sentences.append(lines[sentence].strip('\n'))
    pass


def resolve(query):
    return resolveIfLiteralPresent(query) or resolveByImplication(query) or resolveByOrElimination(query)



def findImplicationSentencesInWhichQueryExists(query):
    pass

def negation(term):
    if '~' in term:
        term = term.strip('~')
    else:
        term = '~' + term
    return term

def findMultipleDisjunctSentenceInWhichQueryExists(query):
    for sentence in sentences:
        if(getPredicate(query) in sentence):
            disjunct_list = sentence.split('|')
    neg_disjunct_list = map(negation, disjunct_list)
    return disjunct_list

def resolveByOrElimination(query):
    sentence = findMultipleDisjunctSentenceInWhichQueryExists(query) #TODO do for all such sentences
    for sentence in sentences:
        terms = getNegDisjunctsFromDisjunction(sentence)
        for term in terms:
            if resolve(premise):
                return True
    return False

def resolveByImplication(query):
    premises = findImplicationSentencesInWhichQueryExists(query)
    for premise in premises:
        if resolve(premise):
            return True
    return False

if __name__ == '__main__':
    getInputs()