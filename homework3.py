queries, KB_sentences_master, KB_sentences = [], [], []
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


def reverseMapping(map):
    reverse_map = {v: k for k, v in map.items()}
    return reverse_map


def resolveIfLiteralPresent(query):
    predicate = query.split('(')[0]
    parameters_in_query = getParameterFromTerm(query) # get parameter in ()
    for sentence in KB_sentences:
        if is_single_literal(sentence) and predicate in sentence: # Get single literal sentences
            parameters_in_sentence = getParameterFromTerm(sentence) #get parameter within ()
            if isVariable(parameters_in_sentence) or parameters_in_query == parameters_in_sentence:
                return True
            if isVariable(parameters_in_query) and not isVariable(parameters_in_sentence): # UNIFY here and return the var-const matching
                return getUnifierDict(query, sentence)
    return False

def resolve(query): #TODO add DP
    return resolveIfLiteralPresent(query)  or resolveByOrEliminationForKB(query) #or resolveByImplication(query)

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
        if not(term_params[i] == query_params[i]):
            #variable_constant_pair = getVariableConstantPair(query_params[i], term_params[i]) # to reorder as {variable : constant} or {var1 : var2},
            unifiers[query_params[i]] = term_params[i]                     # param order matters here for getVarConstPair()
    return unifiers

def findImplicationSentencesInWhichQueryExists(query):
    implicationSentences, implication_sentences_with_unification = [], []
    for sentence in KB_sentences:
        if len(sentence.split('|')) == 2: #Sentence capable of being in implication form
            conclusion = sentence.split('|')[1]
            if getPredicate(query) in conclusion: # Sentence has query as conclusion
                query_params = getParameterFromTerm(query)
                conclusion_params = getParameterFromTerm(conclusion)
                if query_params == conclusion_params or (isVariable(query_params) and isVariable(conclusion_params)):
                    implicationSentences.append(sentence) # When query matches conclusion in simple way
                else:
                    if getUnifierDict(query, conclusion):
                        implication_sentences_with_unification.append(sentence) # When query matches conclusion after unification

    return implicationSentences, implication_sentences_with_unification

def apply_unifiers(term, unifiers):
    predicate = getPredicate(term)
    params = getParameterFromTerm(term)
    for key in unifiers:
        params = params.replace(key, unifiers[key])
    return predicate + '(' + params + ')'

def resolveByImplication(query):
    implication_sentences, implication_sentences_with_unification = findImplicationSentencesInWhichQueryExists(query)
    for implication_sentence in implication_sentences:
        premise, conclusion = get_premise_and_conclusion(implication_sentence)
        result_of_resolve_premise_call = resolve(premise)
        if result_of_resolve_premise_call:
            return result_of_resolve_premise_call

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


def getMatchingTerm(query, disjunct_list):
    for disjunct in disjunct_list:
        if getPredicate(query) == getPredicate(disjunct):
            return disjunct
    raise ValueError('Discrepancy in orElimination')


def findDNFInWhichQueryExists(query, sentence):
    if getPredicate(query) in sentence and negation(getPredicate(query)) not in sentence: #TODO Should solve even if just neg(query) present?
        #if unificationNeeded(query, sentence):
            #pass#do something
        disjunct_list = sentence.split('|')

        disjunct_list = list(map(str.strip, disjunct_list))
        corresponding_disjunct = disjunct_list[-1]#getMatchingTerm(query, disjunct_list)
        disjunct_list.remove(corresponding_disjunct)
        neg_disjunct_list = list(map(negation, disjunct_list))
        return neg_disjunct_list, corresponding_disjunct
    return None, None


def applyTransitiveOperation(pre_unifier_list, unifier_list):

    for key in pre_unifier_list:
        if pre_unifier_list[key] in unifier_list:
            pre_unifier_list[key] = unifier_list[pre_unifier_list[key]]

def removeVariableMappingsInUnifierList(pre_unifier_list):
    return {key: value for key, value in pre_unifier_list.items() if not (isVariable(key) and isVariable(value))}

def resolveByOrEliminationForKB(query):
    for sentence in KB_sentences: #TODO instead of looping all sentences, fetch from pre-indexed list where query is present
        resolve_result = resolveByOrElimination(query, sentence)
        if resolve_result:
            return resolve_result
    return False


def removeConstantAsKeyItems(unifier_list):
    unifier_list_clone = unifier_list.copy() # cloning to prevent concurrent_modification_exception
    for key in unifier_list:
        if not isVariable(key):
            del unifier_list_clone[key]
    return unifier_list_clone

def resolveByOrElimination(query, sentence):
    #KB_sentences.remove(sentence)
    neg_disjuncts, corresponding_disjunct = findDNFInWhichQueryExists(query, sentence)
    if not neg_disjuncts: # there is no sentence with multiple disjuncts
        return False

    pre_unifier_list = getUnifierDict(query, corresponding_disjunct)
    unifier_list = reverseMapping(removeVariableMappingsInUnifierList(pre_unifier_list)) # filtering var-var unifications
    unifier_list = removeConstantAsKeyItems(unifier_list)
    for neg_disjunct in neg_disjuncts:
        neg_disjunct = apply_unifiers(neg_disjunct, unifier_list)
        result = resolve(neg_disjunct)
        if not result:
            return False
        elif not type(result) == type(True):
            unifier_list.update(result)
    applyTransitiveOperation(pre_unifier_list, unifier_list)
    #pre_unifier_list = removeConstantAsKeyItems(pre_unifier_list)
    return pre_unifier_list

def get_premise_and_conclusion(implication_sentence):
    parts = implication_sentence.split('|')
    return negation(parts[0].strip()), parts[1].strip()


if __name__ == '__main__':
    getInputs(queries, KB_sentences, 'input.txt')
    for query in queries:
        print(resolve(query))