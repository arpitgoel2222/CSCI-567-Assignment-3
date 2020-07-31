import sys

infile = open("input.txt", "r")
outfile = open('output.txt', 'w')

dictforchain = {}
def backwardask(kb, query):
    closed.clear()
    i=1
    dict = {}
    s = backwardor(kb, query, dict)
    #i=i+int(s)
    # check each query in the kb for chaining backward
    if i==0:
        return "Invalid"
    for k in s:
        if Correct in k and Wrong not in k:
            return "TRUE"
        elif Wrong in k:
            continue
        elif i==0:
            return "Invalid"
    return "FALSE"

closed={}
queries = []
kb = {}

def unification(x, y, subst):
    #print(x,y)
    dic={}#stores values for unification
    if x == y:
        return subst
    if subst:
        if Wrong in subst:
            return subst
    # first checking for variables
    if y.islower() and not "," in y and not "(" in y:
        if occ(y,x,subst):
            subst[Wrong]=Wrong
        elif y in subst.keys():
        # unification of variable
            unification(subst[y],x,subst)
        else:
            if "(" in x:
                for k in vget(arguments(x)):
                #search in keys
                    if k in subst.keys():
                        statement=replace(k,subst[k],x)
            #print(x)
            subst[y]=x
    elif x.islower() and not "," in x and not "(" in x:
        if occ(x,y,subst):
            subst[Wrong]=Wrong
        elif x in subst.keys():
        # unification of variable
            unification(subst[x],y,subst)
        else:
        # else directly put value of variable in the clause
            if "(" in y:
                for k in vget(arguments(y)):
                #search in keys
                    if k in subst.keys():
                        statement=replace(k,subst[k],y)
            #print(y)
            subst[x]=y
    # case of compund
    elif "(" in x and "(" in y:
        one=x[0:x.find("(")]
        second=y[0:y.find("(")]
        unification(one, second, subst)
        return unification(arguments(x), arguments(y), subst)
    # another case of lst
    elif "," in x and "," in y:
    #for x
        if not "(" in x:
            firsta=x[0:x.find(",")]
            resta=x[x.find(",")+1:len(x)]
        else:
            firsta=x[0:x.find(")")+1]
            resta=x[x.find(")")+2:len(x)]
    #for y
        if not "(" in y:
            firstb=y[0:y.find(",")]
            restb=y[y.find(",")+1:len(y)]
        else:
            firstb=y[0:y.find(")")+1]
            restb=y[y.find(")")+2:len(y)]
        #print(firsta,resta,firstb,restb)
        unification(firsta, firstb, subst)
        return unification(resta, restb, subst)
    #if nothing works
    else:
        subst[Wrong] = Wrong
        return subst

def cnf(i,term):
    cnflist = []
    args = arguments(term).split(",")
    # converting the sentence into cnf starts
    for v in args:
        if v.islower() and "," not in v and "(" not in v:
            cnflist.append(v + str(i))
        else:
            cnflist.append(v)
    term = term[0:term.find("(")] + "("+",".join(cnflist)+")"
    #print(term)
    # sentence after converting into cnf
    return term

Wrong = "failure"
Correct = "True"
kbqueries= {}


# backward chaining of or operator
def backwardor(kb, query, subst):
    lists = []
    operator = query[0:query.find("(")]
    #print(operator)
    f = 0
    if query in kb and Correct in kb[query]:
        closed.pop(query, None)
        subst[Correct] = Correct
        #closed.pop(query, None)
        lists.append(subst)
        #print(list)
        return lists
    # check if goal already in list closed
    if query in closed:
        subst[Wrong] = Wrong
        lists.append(subst)
        #print(list)
        return lists
    # checking for a fact in the knowledge base
    if truestatement(query):
        closed[query] = Correct
        #print(closed)
    given = {k: v for k, v in kb.items() if operator == k[0:k.find("(")]}
    for second,first in given.items():
        f = 1
        for l in first:
            temp = {}
            #do the unification
            if l == Correct:
                unification(second, query, temp)
                backwardand(kb, query, temp)
            else:
                unification(second, query, temp)
                backwardand(kb, l, temp)
            if Wrong not in temp and Correct in temp:
                temp.update(subst)
                lists.append(temp)
                closed.pop(query, None)
    if f != 1 or not lists:
        subst[Wrong] = Wrong
        lists.append(subst)
        #print(list)
    return lists

#backeard chaining for and operators
def backwardand(kb, query, sl):
    #if no queries
    if len(query)==0:
        return s1
    elif sl and Wrong in sl:
        return sl
    else:
        f=1
        v = dict.copy(sl)
        goal1 = query.split("^")
        ft = goal1[0]
        goal1.remove(ft)
        #print(g1) this should not have ^ 'this'
        rest = "^"
        #join the string with the other half
        rest=rest.join(goal1)
        ft = subst(ft, sl)
        l = backwardor(kb, ft, sl)
        for s in l:
            if Correct in s and Wrong not in s:
                f=0
                sl.update(s)
            if rest and Wrong not in s:
                backwardand(kb, rest, s)
            #print(f)
        if f != 0:
            sl[Wrong] = Wrong
        return sl

def occ(var, x, s):
    #if same then answer
    if var == x:
        return True
    elif "(" in x:
    #recursive solve for beackets
        return (occ(var, arguments(x), s)) or occ(var, x[0:x.find("(")], s)
    elif x.islower() and not "," in x and not "(" in x and x in s:
    #recursive solve for varibales
        return occ(var, s[x], s)
    else:
        return False

def arguments(clause):
    if "(" in clause:
        count=0
        count=count+1
        #print(count)
        return clause[clause.find("(")+1:len(clause)-1]


def subst(ss, slist):
    #first checking for brackets and commas
    if "(" in ss:
        aa= ss[ss.find("(")+1:len(ss)-1]
    args = arguments(ss).split(',')
    #print(args)
    for k in args:
        #first check for variable
        if k.islower() and not "," in k and not "(" in k:
            if k in slist.keys():
                sv = slist[k]
                count=1
                if sv.islower() and not "," in sv and not "(" in sv and sv in slist:
                    sv = slist[sv]
                    count=count+1
                for n, i in enumerate(args):
                    if i == k:
                        args[n] = sv
                        count=count-1
                ss = ss[0:ss.find("(")] + '(' + ','.join(args) + ')'
        elif "(" in k:
            subst(ss, slist)
            mynumber=0
            mynumber=mynumber +1
    #print(ss)
    return ss


listofvalues=[]

#for sentence alreasy in knowledge base
def truestatement(clause):
    a= clause[0:len(clause)-1]
    for l in arguments(clause).split(","):
        #check for v
        if l.islower() and not "," in l and not "(" in l:
            return False
    return True

#finding out variables in the sentence
def vget(str_args):
    a= str_args[0:len(str_args)-1]
    terms = str_args.split(",")
    #print(args)
    for arg in terms:
        #checking if arg is not a part of v
        if not arg.islower() and "," in arg and "(" in arg:
            terms.remove(arg)
    return terms


def replace(variable, val,term):
    #replace variable with values
    new_var=variable
    if "(" in term:
        for value in arguments(term).split(","):
            #check for b and c
            if "(" in arg:
                listofvalues.append(replace(value, variable, val))
            # else check for v
            elif value.islower() and not "," in value and not "(" in value and value == variable:
                listofvalues.append(val)
            else:
                listofvalues.append(value)
        default = term;
        new_var=0
        a= term[0:term.find("(")]
        term = a+"("+",".join(listofvalues)+")"
        #print(term)
    return term


def main():
    no_of_queries= int(infile.readline())
    for i in range(no_of_queries):
        queries.append(infile.readline().strip())
    no_of_sentences= int(infile.readline())
    for i in range(no_of_sentences):
        sentence = infile.readline().strip()
        sentence = sentence.replace(" ", "")
        #checking for implicaton
        if not ">" in sentence:
            value = Correct
            key = sentence[0:sentence.find(")")+1]
            kb.setdefault(key, []).append(value)
        else:
            t = []
            sentence.split(">")
            #find part of sentences
            first = sentence[0:sentence.find(">")-1]
            second = sentence[sentence.find(">")+1:len(sentence)]
            k = cnf(i,second)
            #print(keys)
            for c in first.split("^"):
                t.append(cnf(i,c))
                #print(t)
            v = "^"
            #print v
            v=v.join(t)
            #print v
            kb.setdefault(k, []).append(v)
    answer(kb,queries)
    
def answer(kb,queries):
    # checking each query in the question
    for q in queries:
        try:
            results = backwardask(kb, q)
        except:
            results = "FALSE"
        print (results)
        #printing the ouptut
        outfile.write(results+"\n")

main()

