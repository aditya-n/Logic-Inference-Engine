queries, sentences = [], []
KB = {}

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

def isVariable(parameter):
    list_of_parameters = parameter.split(',')
    for parameter in list_of_parameters:
        if parameter[0].isupper():
            return False
    return True


def canUnify(parameter_in_sentence, parameter_in_query):
    if len(parameter_in_query) != len(parameter_in_sentence):
        return False


def resolveIfLiteralPresent(query):
    predicate = query.split('(')[0]
    parameter_in_query = query[query.find("(")+1:query.find(")")] # get parameter in ()
    for sentence in sentences:
        if is_single_literal(sentence) and predicate in sentence: # Get single literal sentences
            parameter_in_sentence = sentence[sentence.find("(")+1:sentence.find(")")] #get parameter within ()
            if isVariable(parameter_in_sentence) or parameter_in_query == parameter_in_sentence:
                return True
    return False

def resolve(query): #TODO add DP
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


def unificationNeeded(query, sentence):
    pass #if query in sentence: #TODO is this needed?


def findDNFInWhichQueryExists(query):
    for sentence in sentences:
        if getPredicate(query) in sentence and negation(getPredicate(query)) not in sentence:
            if unificationNeeded(query, sentence):
                pass#do something
            disjunct_list = sentence.split('|')
            disjunct_list = list(map(str.strip, disjunct_list))[:-1] # TODO need not be the last always
            neg_disjunct_list = list(map(negation, disjunct_list))
            return neg_disjunct_list
    return []

def resolveByOrElimination(query):
    neg_disjuncts = findDNFInWhichQueryExists(query) #TODO do for all such sentences
    if not neg_disjuncts: # there is no sentence with multiple disjuncts
        return False
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