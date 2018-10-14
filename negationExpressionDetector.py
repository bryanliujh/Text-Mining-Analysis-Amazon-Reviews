import nltk
import negationWordDetector
import re

def detectNegation(words):
    #foundNegation and index lists for debugging
    foundNegation = []
    index=[]
    #clause to store actual output
    clause = []
    loc=0
    tags = nltk.pos_tag(words)
    for word in words:
        searchObject = negationWordDetector.detectCompleteNegationWord(word)
        if searchObject:
            foundNegation.append(word)
            index.append(loc)
            clause.append(decideClauseComponent(loc, tags))
        else:
            searchObject2 = negationWordDetector.detectShortFormNegationWord(word)
            if searchObject2:
                foundNegation.append(words[loc-1]+ "n't")
                index.append(loc)
                clause.append(decideClauseComponent(loc, tags))
        loc = loc+1
    #return dict(zip(foundNegation, index))
    return clause


def decideClauseComponent(loc, tags):
    word = tags[loc][0].lower()
    if re.search("^no+t?$", word):
        word = word + "_"
    functDic ={
        "no_": findClauseContainingNo,
        "n't": findClauseContainingSF,
        "not_": findClauseContainingNot,
        "never": findClauseContainingNever,
        "none": findClauseContainingNone,
        "nobody": returnWord,
        "nothing": returnWord,
    }
    if re.search("^no+_$", word):
        word= "no_"
    elif re.search("^no+t_$", word):
        word= "not_"
    elif re.search("^no+ne$", word):
        word= "none"
    elif re.search("n't", word):
        word = "n't"
    elif re.search("^no+thing", word):
        word= "nothing"
    elif re.search("^never", word):
        word= "never"
    if word in ["no_", "n't", "not_", "never", "none", "nobody", "nothing"]:
        return functDic[word](loc, tags)
    else:
        return [word]

#append negation word with tokenized words until end of noun phrase is reached
def appendTillNoun(loc, tags, clause):
    #match NN, NNS, NNP, NNPS out of available tags
    hit = False
    for i in range(loc+1, len(tags)):
        if (hit==False and not re.search(",|\\.", tags[i][1])) or (hit==True and re.search("(NN)|(PRP)", tags[i][1])):
            clause = clause + " "+ tags[i][0]
        else:
            break
        if re.search("(NN)|(PRP$)", tags[i][1]) :
            hit = True
    return clause

#append negation word with verb followed, if particle or adverb exists, append it too
def appendVerb(loc, tags, clause):
    clause = clause + " "+ tags[loc+1][0]
    #^RP$ matches particle, ^RB matches RB, RBR, RBS but not WRB
    if loc+2<len(tags) and re.search("(^RP$)|(^RB)", tags[loc+2][1]):
        clause = clause + " " +tags[loc+2][0]
    return clause

#detect expression started with adverb and append it with negation
def detectExpressionStartedWIthRB(loc, tags, clause):
    clause = clause + " " + tags[loc+1][0]
    if loc+2<len(tags):
        if re.search("VB", tags[loc+2][1]):
            clause = appendVerb(loc+1, tags, clause)
        elif re.search("(JJ)|(^RB)", tags[loc+2][1]):
            clause = clause + " " + tags[loc+2][0]
        #CD is cardinal number
        elif re.search("(DT)|(CD)", tags[loc+2][1]):
            clause = appendTillNoun(loc+1, tags, clause)
    return clause

def findClauseContainingNo(loc, tags):
    clause = tags[loc][0]
    return appendTillNoun(loc, tags, clause)

def findClauseContainingSF(loc, tags):
    #combine the n't with the word before it
    clause = tags[loc-1][0] + tags[loc][0]
    if loc+1<len(tags):
        #n't followed by verb is more possible to appear
        if re.search("VB", tags[loc+1][1]):
            clause = appendVerb(loc, tags, clause)
        #n't followed by adverb
        elif re.search("^RB", tags[loc+1][1]):
            clause = detectExpressionStartedWIthRB(loc, tags, clause)
        #n't followed by adjective
        elif re.search("JJ", tags[loc+1][1]):
            clause = clause + " "+ tags[loc+1][0]
        #n't followed by noun phrase is least possible to appear
        elif re.search("(DT)|(IN)|(PRP)|(NN)", tags[loc+1][1]):
            clause = clause + " "+ tags[loc+1][0]
            clause = appendTillNoun(loc+1, tags, clause)
    return clause

def findClauseContainingNot(loc, tags):
    clause = tags[loc][0]
    if loc+1<len(tags):
        #not followed by noun phrase is more possible to appear
        if re.search("(DT)|(IN)|(PRP)|(NN)", tags[loc+1][1]):
            #not followed by maybe a/an/the, then adjective then noun
            clause = clause + " " + tags[loc+1][0]
            clause = appendTillNoun(loc+1, tags, clause)
        #not followed by adverb
        elif re.search("^RB", tags[loc+1][1]):
            clause = detectExpressionStartedWIthRB(loc, tags, clause)
        #not followed by verb
        elif re.search("VB", tags[loc+1][1]):
            clause = appendVerb(loc, tags, clause)
        #not followed by adjective
        elif re.search("JJ", tags[loc+1][1]):
            clause = clause + " " + tags[loc+1][0]
        #not followed by word 'to'
        elif re.search("TO", tags[loc+1][1]):
            clause = clause + " " + tags[loc+1][0]
            if loc+2<len(tags):
                if re.search("VB", tags[loc+2][1]):
                    clause = appendVerb(loc+1, tags, clause)
                else:
                    clause = appendTillNoun(loc+1, tags,clause)
    return clause

def findClauseContainingNever(loc, tags):
    clause = tags[loc][0]
    if loc+1<len(tags):
        #never followed by verb is more likely to appear
        if re.search("VB", tags[loc+1][1]):
            clause = appendVerb(loc, tags, clause)
        #never followed by adverb
        elif re.search("^RB", tags[loc+1][1]):
            clause = detectExpressionStartedWIthRB(loc, tags, clause)
        #never followed by adjective
        elif re.search("JJ", tags[loc+1][1]):
            clause = clause + " " + tags[loc+1][0]
    return clause

def findClauseContainingNone(loc, tags):
    clause = tags[loc][0]
    #append the words till noun phrase is found
    if re.search("NN", tags[loc][1]):
        return appendTillNoun(loc, tags, clause)
    elif re.search("^RB", tags[loc][1]):
        return detectExpressionStartedWIthRB(loc, tags, clause)
    else:
        return clause

#for negation word 'nobody' and 'nothing', simply return the single word as negation expression
def returnWord(loc, tags):
    return tags[loc][0]


