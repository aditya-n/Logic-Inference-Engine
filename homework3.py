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

def getParameterFromTerm(term):
    return term[term.find("(") + 1:term.find(")")]

def resolveIfLiteralPresent(query):
    predicate = query.split('(')[0]
    parameters_in_query = getParameterFromTerm(query) # get parameter in ()
    for sentence in sentences:
        if is_single_literal(sentence) and predicate in sentence: # Get single literal sentences
            parameters_in_sentence = getParameterFromTerm(sentence) #get parameter within ()
            if isVariable(parameters_in_sentence) or parameters_in_query == parameters_in_sentence:
                return True
            if isVariable(parameters_in_query) and not isVariable(parameters_in_sentence): # UNIFY here and return the var-const matching
                return getUnifierDict(query, predicate)
    return False

def resolve(query): #TODO add DP
    return resolveIfLiteralPresent(query) or resolveByImplication(query) or resolveByOrElimination(query)

def getUnifierDict(query, term):
    unifiers = {}
    if getPredicate(query) != getPredicate(term):
        return None
    query_params = getParameterFromTerm(query).split(',')
    term_params = getParameterFromTerm(term).split(',')
    if query_params == term_params:
        return term
    no_of_params = len(query_params)
    for i in range(0, no_of_params):
        if not (isVariable(term_params[i]) and isVariable(query_params[i])):
            getVariableConstantPair(term_params[i], query_params[i]) #TODO COmplete imme
            unifiers[term_params[i]] = query_params[i]
    return unifiers

def findImplicationSentencesInWhichQueryExists(query):
    implicationSentences = []
    for sentence in sentences:
        if len(sentence.split('|')) == 2:
            conclusion = sentence.split('|')[1]
            if getPredicate(query) in conclusion:
                getUnifierDict(query, conclusion)
                implicationSentences.append(sentence)
    return implicationSentences

def negation(term):
    return term.strip('~') if '~' in term else '~' + term

def getPredicate(query):
    return query.split('(')[0]

def unificationNeeded(query, sentence):
    pass #if query in sentence: #TODO is this needed?

def findDNFInWhichQueryExists(query):
    for sentence in sentences: #TODO instead of looping all sentences, fetch from pre-indexed list where query is present
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