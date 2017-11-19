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


def updateDict(unifier_list, new_unifiers):
    for key in new_unifiers:
        if key in unifier_list:
            unifier_list[key] = unifier_list[key] + '&' + new_unifiers[key]
        else:
            unifier_list[key] = new_unifiers[key]

def resolveIfLiteralPresent(query):
    predicate = getPredicate(query)
    parameters_in_query = getParameterFromTerm(query) # get parameter in ()
    unifier_list = {}
    for sentence in KB_sentences:
        if is_single_literal(sentence) and predicate == getPredicate(sentence): # Get single literal sentences
            parameters_in_sentence = getParameterFromTerm(sentence) #get parameter within ()
            if isVariable(parameters_in_sentence) or parameters_in_query == parameters_in_sentence:
                return True
            if isVariable(parameters_in_query) and not isVariable(parameters_in_sentence): # UNIFY here and return the var-const matching
                temp_unifier_list = getUnifierDict(query, sentence) #Hack for preventing one var mapping to multiple constants
                if temp_unifier_list is None:                       #
                    return False                                    #
                updateDict(unifier_list, temp_unifier_list)
    if unifier_list:
        return unifier_list
    else:
        return False

def resolve(query, sentence_set): #TODO add DP
    new_sentence_set = sentence_set.copy()
    if query in new_sentence_set:
        return False
    new_sentence_set.add(query)
    return resolveIfLiteralPresent(query)  or resolveByOrEliminationForKB(query, new_sentence_set) # or resolveByImplication(query) #implication is a specific case of orElim

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
            if not isVariable(term_params[i]) and not isVariable(query_params[i]): # when match is between 2 unequal constants
                return None                                                            # There is no unification for the whole query and term
            else:
                if query_params[i] in unifiers and unifiers[query_params[i]] != term_params[i]: # if single var maps to multiple constants . Do(x,x) , Do(Jaga,Laya)
                    return None
                unifiers[query_params[i]] = term_params[i]   # param order matters here for getVarConstPair()
    return unifiers


def apply_unifiers(term, unifiers):
    predicate = getPredicate(term)
    params = getParameterFromTerm(term)
    params_list = params.split(',')

    new_params_list = [unifiers[param] if param in unifiers else param for param in params_list]

    return predicate + '(' + ','.join(new_params_list) + ')'

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
    disjunct_list = sentence.split('|')
    disjunct_list = list(map(str.strip, disjunct_list))
    corresponding_disjunct = None
    for disjunct in disjunct_list:
        if getPredicate(query) == getPredicate(disjunct) and getUnifierDict(query, disjunct) is not None:  #TODO Should solve even if just neg(query) present?
            corresponding_disjunct = disjunct #getMatchingTerm(query, disjunct_list)
    if corresponding_disjunct:
        disjunct_list.remove(corresponding_disjunct)
        neg_disjunct_list = list(map(negation, disjunct_list))
        return neg_disjunct_list, corresponding_disjunct
    return None, None

def applyTransitiveOperation(pre_unifier_list, unifier_list):

    for key in pre_unifier_list:
        if pre_unifier_list[key] in unifier_list:
            temp = pre_unifier_list[key]
            pre_unifier_list[key] = unifier_list[pre_unifier_list[key]]
            del unifier_list[temp]

def removeVariableMappingsInUnifierList(pre_unifier_list):
    return {key: value for key, value in pre_unifier_list.items() if not (isVariable(key) and isVariable(value))}

def resolveByOrEliminationForKB(query, sentence_set):
    for sentence in KB_sentences: #TODO instead of looping all sentences, fetch from pre-indexed list where query is present
        resolve_result = resolveByOrElimination(query, sentence, sentence_set)
        if resolve_result:
            return resolve_result
    return False


def removeConstantAsKeyItems(unifier_list):
    unifier_list_clone = unifier_list.copy() # cloning to prevent concurrent_modification_exception
    for key in unifier_list:
        if not isVariable(key):
            del unifier_list_clone[key]
    return unifier_list_clone


def getMultiValuedKeyIfPresentInDict(unifier_list_for_this_disjunct):
    for key in unifier_list_for_this_disjunct:
        if '&' in unifier_list_for_this_disjunct[key]: #TODO what if multiple keys have multiple values
            return key
    return False

def getUpdatedUnifierListForMultiValuedKeys(unifier_list, neg_disjuncts, index, sentence_set):
    new_unifier_list = unifier_list.copy()
    new_neg_disjuncts = neg_disjuncts.copy()
    if index == len(new_neg_disjuncts):
        return unifier_list

    new_neg_disjuncts[index] = apply_unifiers(new_neg_disjuncts[index], new_unifier_list)
    unifier_list_for_this_disjunct = resolve(new_neg_disjuncts[index], sentence_set)

    if not unifier_list_for_this_disjunct:
        return None
    elif type(unifier_list_for_this_disjunct) == type(True):
        return getUpdatedUnifierListForMultiValuedKeys(new_unifier_list, new_neg_disjuncts, index + 1, sentence_set)

    new_unifier_list.update(unifier_list_for_this_disjunct)

    multi_valued_key = getMultiValuedKeyIfPresentInDict(unifier_list_for_this_disjunct)
    if multi_valued_key:
        branch_values = unifier_list_for_this_disjunct[multi_valued_key].split('&')
        for value in branch_values:
            del new_unifier_list[multi_valued_key]
            new_unifier_list.update({multi_valued_key : value})
            result = getUpdatedUnifierListForMultiValuedKeys(new_unifier_list, new_neg_disjuncts, index + 1, sentence_set)
            if result:
                return result
        return None
    else:
        return getUpdatedUnifierListForMultiValuedKeys(new_unifier_list, new_neg_disjuncts, index + 1, sentence_set)
        #raise ValueError('WHY NOT MULTIVALUED') # Why did your code arrive here? HUHHHHHHHHHHHHHHHHHHHHH?


def getUnifierListForNegDisjunctList(unifier_list, neg_disjuncts, sentence_set):
    for index, neg_disjunct in enumerate(neg_disjuncts):
        neg_disjunct = apply_unifiers(neg_disjunct, unifier_list)
        result = resolve(neg_disjunct, sentence_set)
        if not result: #Case : Can't unify
            return None
        elif not type(result) == type(True): #Case: one variable unifies to multipl constants
            if getMultiValuedKeyIfPresentInDict(result):
                return getUpdatedUnifierListForMultiValuedKeys(unifier_list, neg_disjuncts, index, sentence_set) # do something
            else:                            #Case: normal
                unifier_list.update(result)
    return unifier_list


def removeUnnecessaryVariables(pre_unifier_list, query):
    pre_unifier_list_copy = pre_unifier_list.copy()
    query_params = getParameterFromTerm(query)
    for key in pre_unifier_list:
        if key not in query_params:
            del pre_unifier_list_copy[key]
    return pre_unifier_list_copy

def resolveByOrElimination(query, sentence, sentence_set):
    neg_disjuncts, corresponding_disjunct = findDNFInWhichQueryExists(query, sentence)
    if not neg_disjuncts: # there is no sentence with multiple disjuncts
        return False

    pre_unifier_list = getUnifierDict(query, corresponding_disjunct)
    unifier_list = reverseMapping(removeVariableMappingsInUnifierList(pre_unifier_list)) # filtering var-var unifications
    unifier_list = removeConstantAsKeyItems(unifier_list)

    unifier_list = getUnifierListForNegDisjunctList(unifier_list, neg_disjuncts, sentence_set)
    if unifier_list is None:
        return False

    applyTransitiveOperation(pre_unifier_list, unifier_list)
    pre_unifier_list.update(unifier_list)
    pre_unifier_list = removeUnnecessaryVariables(pre_unifier_list, query)
    if not pre_unifier_list:
        return True
    return pre_unifier_list

def resultInCorrectOutputFormat(query):
    return "TRUE" if resolve(query, set()) else "FALSE"

if __name__ == '__main__':
    getInputs(queries, KB_sentences, 'input.txt')
    file = open('output.txt', 'w')
    for query in queries:
        result = resultInCorrectOutputFormat(query)
        #print(result)
        file.write(result+'\n')
    file.close()