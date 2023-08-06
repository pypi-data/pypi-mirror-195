# parse methods for mujpy func
# a string, e.g. func0 = 'p[2]*exp(p[5]/p[0])' must be:
# 1) parsed for correct syntax
# 2) indices substituted according to a given correspondence jk = mindex(k)
#      to yield 'p[j2]*exp(p[j5]/p[j0])'
# 3) compiled into method meth0(p0,p1,p2), with three parameters
# the string func1 = 'p[3]' will result in 'p[j3]' and point to def meth(p0): return p0

# Possible project:
#  a parser distinguishes single out
#  numerical constants, parameters, 1d functions (), constants, binary operators (*,/,-,+,^,>,<,...)
#  parameters are remapped and stored, numerical constants are stored, binops are mapped to functions 
# all functions are mapped to methods, the procedure cascades up to a single method, 
# the single method is passed to mucomponents
# Equation 1.3 parses functions, binops and constants, 
# does not parse array/list indices [0], has limited set of functions
# array indices may be sorted before, function set may be extended


def parse(function):
    '''
    parses strings like
    "p[2]*exp(p[5]/p[0])"
    to check for syntax

    '''
    try: 
    except:
        return -1
    return 0

def muvalid(string,mindex):
    '''
    parse function CHECK WITH MUCOMPONENT, THAT USES A DIFFERENT SCHEME
    accepted functions are RHS of agebraic expressions of parameters p[i], i=0...ntot  
    '''
    import re

    string = string.replace(" ", "")  #  removes all blanks
    pattern = re.findall(r"\p\[(\d+)\]",string) # find all patterns p[*] where * is digits and extracts digits
    repattern = [str(mindex[int(k)]) for k in pattern.findall(string)]
    for pat, rep in zip(patt,repattern):
        string = re.sub(pat,rep,string) # index replaced according to mindex
    

    try: 
        safetry(test) # should select only safe use (although such a thing does not exist!)
    except Exception as e:
        with out:
            print('function: {}. Tested: {}. Wrong or not allowed syntax: {}'.format(string,test,e))
        index = 3
        valid = False
    return valid

def set_dict():
    '''
    returns dictionary of functions, binary operators and constants
    func['cos'](a) = cos(a) ...
    bop['^'](a,b) = pow(a,b) ...
    const['pi'] = 3.141592 ...
    '''
    from math import acos,asin,atan,atan2,cos,cosh,exp,log,log10,pi,sin,sinh,sqrt,tan,tanh
    from operator import mul, truediv, add, sub
    # pow, abs are built-in
    functions = ['abs','acos', 'asin', 'atan', 'atan2', 'cos', 'cosh', 
                 'exp', 'log', 'log10', 'sin', 'sinh', 
                 'sqrt', 'tan', 'tanh'] 
    binops = [ 'pow', 'mul', 'truediv', 'add', 'sub']
    symbols = ['^','*','/','+','-']
    constants = ['pi','gamu','gae']
    gamu, gae = 135.5, 2802.5 # MHz/T
    # 	use the list to filter the local namespace
    func = {}
    for k in functions:
        func.update({k:eval(k)}) # so if string = 'cos' and angle = 0.85 func[string](angle) is cos(angle)
    bop = {}
    for k,j in zip(symbols,binops):
        bop.update({k,eval(j)}) # so if string = '^', a=10., b = 2. bop[string](a,b) is pow(a,b)
    const = {}
    for k in constants:
        const.update({k,eval(k)})
    return func, bop, const


