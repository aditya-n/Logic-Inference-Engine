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
        if parameter[0].islower():
            return True
    return False

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
                return getUnifierDict(query, sentence)
    return False

def resolve(query): #TODO add DP
    return resolveIfLiteralPresent(query) or resolveByImplication(query) or resolveByOrElimination(query)

def getVariableConstantPair(param1, param2):
        return (param1, param2) if isVariable(param1) else (param2, param1)

def getUnifierDict(query, term):
    unifiers = {}
    if getPredicate(query) != getPredicate(term):
        return None
    query_params = getParameterFromTerm(query).split(',')
    term_params = getParameterFromTerm(term).split(',')
    if query_params == term_params:
        return {}
    no_of_params = len(query_params)
    for i in range(0, no_of_params):
        if not (isVariable(term_params[i]) and isVariable(query_params[i])):
            variable_constant_pair = getVariableConstantPair(term_params[i], query_params[i]) # to reorder as {variable : constant}
            unifiers[variable_constant_pair[0]] = variable_constant_pair[1]
    return unifiers

def findImplicationSentencesInWhichQueryExists(query):
    implicationSentences, implication_sentences_with_unification = [], []
    for sentence in sentences:
        if len(sentence.split('|')) == 2: #Sentence capable of being in implication form
            conclusion = sentence.split('|')[1]
            if getPredicate(query) in conclusion:
                query_params = getParameterFromTerm(query)
                conclusion_params = getParameterFromTerm(conclusion)
                if query_params == conclusion_params or (isVariable(query_params) and isVariable(conclusion_params)):
                    implicationSentences.append(sentence) # When query matches conclusion in simple way
                else:
                    if not getUnifierDict(query, conclusion):
                        implication_sentences_with_unification.append(sentence) # When query matches conclusion after unification

    return implicationSentences, implication_sentences_with_unification

def apply_unifiers(term, unifiers):
    for key in unifiers:
        term = term.replace(key, unifiers[key])
    return term

def resolveByImplication(query):
    implication_sentences, implication_sentences_with_unification = findImplicationSentencesInWhichQueryExists(query)
    for implication_sentence in implication_sentences:
        premise, conclusion = get_premise_and_conclusion(implication_sentence)
        result_resolve_premise = resolve(premise)
        if result_resolve_premise:
            return result_resolve_premise

    for implication_sentence in implication_sentences_with_unification:
        premise, conclusion = get_premise_and_conclusion(implication_sentence)
        unifier_list = getUnifierDict(query, conclusion)
        premise = apply_unifiers(premise, unifier_list)
        if resolve(premise):
            return unifier_list
    return False

def negation(term): #TODO implement to solve neg(query)
    return term.strip('~') if '~' in term else '~' + term

def getPredicate(query):
    return query.split('(')[0]

def findDNFInWhichQueryExists(query):
    for sentence in sentences: #TODO instead of looping all sentences, fetch from pre-indexed list where query is present
        if getPredicate(query) in sentence and negation(getPredicate(query)) not in sentence:
            #if unificationNeeded(query, sentence):
                #pass#do something
            disjunct_list = sentence.split('|')
            disjunct_list = list(map(str.strip, disjunct_list))[:-1] # TODO need not be the last always
            neg_disjunct_list = list(map(negation, disjunct_list))
            return neg_disjunct_list
    return []

def resolveByOrElimination(query):
    neg_disjuncts = findDNFInWhichQueryExists(query) #TODO do for all such sentences
    if not neg_disjuncts: # there is no sentence with multiple disjuncts
        return False
    unifier_list = {}
    for neg_disjunct in neg_disjuncts:
        result = resolve(neg_disjunct)
        if not result:
            return False
        else:
            unifier_list.update(result)
    return unifier_list

def get_premise_and_conclusion(implication_sentence):
    parts = implication_sentence.split('|')
    return negation(parts[0].strip()), parts[1].strip()


if __name__ == '__main__':
    getInputs(queries, sentences, 'input.txt')
    print(resolve('R(x)'))