import ast
from astor import to_source
from sly import Parser
from lex import KLex

def I(n):
    return n

def wrap(n):
    return ast.Call(ast.Name(id="I",ctx=ast.Load()),[n],keywords=[])

def astck(n):
    return to_source(ast.fix_missing_locations(ast.Expression(n)))

class KParse(Parser):
    tokens = KLex.tokens
    precedence = (('right',)+tuple(tokens),)
    pc = 0 # parse count
    asts = []

    @_('expr NEWLINE')
    def root(self,p):
        self.pc+=1
        print(str(self.pc)+":\teN:\t"+astck(p.expr))
        self.pc = 0 # reset PC ready for next expression
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.expr)))
        return self.asts

    @_('paren NEWLINE')
    def root(self,p):
        self.pc+=1
        print(str(self.pc)+":\tpN:\t"+astck(p.paren))
        self.pc = 0 # reset PC ready for next expression
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.paren)))
        return self.asts

    @_('expr SEMI expr')
    def root(self,p):
        self.pc+=1
        #print(str(self.pc)+":\te;e:\t"+astck(p.expr))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.expr0)))
        return p.expr1

    @_('expr SEMI paren')
    def root(self,p):
        self.pc+=1
        #print(str(self.pc)+":\te;e:\t"+astck(p.expr))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.expr)))
        return p.paren

    @_('paren SEMI expr')
    def root(self,p):
        self.pc+=1
        #print(str(self.pc)+":\te;e:\t"+astck(p.expr))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.paren)))
        return p.expr

    @_('paren SEMI paren')
    def root(self,p):
        self.pc+=1
        #print(str(self.pc)+":\tp;p:\t"+astck(p.paren))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.paren0)))
        return self.paren1

    @_('paren SPACE paren')
    def root(self,p):
        self.pc=0
        raise Exception("'typ") # This is what ngn/k does for both `1 (!3)` and `1 (2+3)`
#        self.pc+=1
#        if isinstance(p.paren1,ast.Tuple):
#            n=ast.Tuple(elts=[p.paren0,p.paren1.elts],ctx=ast.Load())
#        else:
#            n=ast.Tuple(elts=[p.paren0,p.paren1],ctx=ast.Load())
#        print(str(self.pc)+":\tpSp:\t"+astck(n)+"\tp0="+astck(p.paren0)+"\tp1="+astck(p.paren1))

    @_('expr SPACE paren')
    def root(self,p):
        self.pc=0
        raise Exception("'typ") # This is what ngn/k does for both `1 (!3)` and `1 (2+3)`
#        self.pc+=1
#        if isinstance(p.expr,ast.Tuple):
#            n=ast.Tuple(elts=[p.expr,p.paren.elts],ctx=ast.Load())
#        else:
#            n=ast.Tuple(elts=[p.expr,p.paren],ctx=ast.Load()) # FIXME: is this right? ngn/k for example throws an error for e.g. 1 (!3)
#        print(str(self.pc+":\teSp:\t"+astck(n)+"\te="+astck(p.expr)+"\tp="+astck(p.paren)))
#        return n

    @_('paren SPACE expr')
    def root(self,p):
        self.pc=0
        raise Exception("'typ") # This is what ngn/k does for both `1 (!3)` and `1 (2+3)`
#        self.pc+=1
#        if isinstance(p.expr,ast.Tuple):
#            n=ast.Tuple(elts=[p.paren,p.expr.elts],ctx=ast.Load())
#        else:
#            n=ast.Tuple(elts=[p.paren,p.expr],ctx=ast.Load())
#        print(str(self.pc+":\tpSe:\t"+astck(n)+"\tp="+astck(p.paren)+"\te="+astck(p.expr)))
#        return n

    @_('expr SPACE expr')
    def tuple(self,p): # FIXME
        self.pc+=1
        print("\te0="+astck(p.expr0)+"\te1="+astck(p.expr1))
        if isinstance(p.expr1,ast.Tuple):
            es=[p.expr0]+p.expr1.elts
        else:
            es=[p.expr0,p.expr1]
        print(str(self.pc)+":\teSe:\t"+astck(ast.Tuple(elts=es,ctx=ast.Load()))+"\te0="+astck(p.expr0)+"\te1="+astck(p.expr1))
        return ast.Tuple(elts=es,ctx=ast.Load())

    @_('PAREN')
    def paren(self,p):
        li= KLex()
        pi = KParse()
        text=p.PAREN[1:-1]
        if text[-1]==";":
            text=text[0:-1]
        print("PAREN:\t"+text)
        r = pi.parse(l.tokenize(text+"\n"))
        self.pc+=1
        if len(r)==1: # TODO: 0?
            print(str(self.pc)+":\t(e):\t"+"TODO: parens") # astck(r[0]))
            return r[0]
        else:
            print(str(self.pc)+":\t(e):\t"+"TODO: multiple expressions")
            return ast.Tuple(elts=r,ctx=ast.Load())

    # TODO: Do we want different cases for ( expr ), ( value ), ( atom ), ( array )?

#    @_('LPAREN expr')
#    def expr(self,p):
#        self.pd-=1
#        print("PD: "+str(self.pd))
#        # FIXME: we need this, but this just fails if we have more than one set of brackets
#        #if self.pd!=0:
#        #    raise Exception("Unbalanced parentheses!") # FIXME: This doesn't detect pd>0 for some reason
#        #else:
#        self.pc+=1
#        print(str(self.pc)+":\t(e:\t"+astck(p.expr))
#        return p.expr
#
#    @_('expr RPAREN')
#    def expr(self,p):
#        self.pd+=1
#        print("PD: "+str(self.pd))
#        self.pc+=1
#        print(str(self.pc)+":\te):\t"+astck(p.expr))
#        return p.expr

#    # TODO: What about e.g. (2);(3), which is legal in ngn/k?
#    #       (Note that (2) (3) is not)
#    @_('expr SEMI expr')
#    def expr(self,p):
##        if self.pd<0:
##            raise Exception("PD is somehow less than 0")
##        elif self.pd==0:
##            return ast.Constant("SEMICOLON-SEPARATED EXPRESSIONS!!") # FIXME
##        else:
##            self.pc+=1
##            print(str(self.pc)+":\te;e:\t"+astck(ast.Tuple(elts=[(p.expr0.elts if isinstance(p.expr0,ast.Tuple) else [p.expr0])+(p.expr1.elts if isinstance(p.expr1,ast.Tuple) else [p.expr1])],ctx=ast.Load()))+"\te0="+astck(p.expr0)+"\te1="+astck(p.expr1))
##            return ast.Tuple(elts=[(p.expr0.elts if isinstance(p.expr0,ast.Tuple) else [p.expr0])+(p.expr1.elts if isinstance(p.expr1,ast.Tuple) else [p.expr1])],ctx=ast.Load()) # FIXME: this won't work for nested tuples, I don't think

    @_('value')
    def expr(self,p):
        self.pc+=1
        print(str(self.pc)+":\tv:\t"+astck(p.value))
        return p.value

    @_('tuple')
    def expr(self,p):
        self.pc+=1
        print(str(self.pc)+":\tl:\t"+astck(p.tuple))
        return p.tuple

    @_('atom')
    def value(self,p):
        self.pc+=1
        print(str(self.pc)+":\ta:\t"+astck(p.atom))
        return p.atom

#    @_('array SPACE array')
#    def array(self,p):
#        return ast.Tuple(elts=(p.array0.elts + p.array1.elts),ctx=ast.Load())

#    @_('atom SPACE tuple')
#    def tuple(self,p):
#        self.pc+=1
#        print(str(self.pc)+":\taSl:\t"+astck(ast.Tuple(elts=([p.atom] + p.tuple.elts),ctx=ast.Load()))+"\ta="+astck(p.atom)+"\tl="+astck(p.tuple))
#        return ast.Tuple(elts=([p.atom] + p.tuple.elts),ctx=ast.Load())
#
##    @_('tuple SPACE atom')
##    def tuple(self,p):
##        return ast.Tuple(elts=(p.tuple.elts + [p.atom]),ctx=ast.Load())
#
#    @_('atom SPACE atom')
#    def tuple(self,p):
#        self.pc+=1
#        print(str(self.pc)+":\taSa:\t"+astck(ast.Tuple(elts=[p.atom0,p.atom1],ctx=ast.Load()))+"\ta0="+astck(p.atom0)+"\ta1="+astck(p.atom1))
#        return ast.Tuple(elts=[p.atom0,p.atom1],ctx=ast.Load())

    @_('NUMBER')
    def atom(self,p):
        self.pc+=1
        print(str(self.pc)+":\tn:\t"+astck(ast.Constant(p.NUMBER))+"\tn="+str(p.NUMBER)+"\n")
        return ast.Constant(p.NUMBER)

    @_('CHAR')
    def atom(self,p):
        if p.CHAR=='q':
            exit(0)
        else:
            self.pc+=1
            print(str(self.pc)+":\tc:\t"+astck(ast.Constant(p.CHAR))+"\tc="+p.CHAR+"\n")
            return ast.Constant(p.CHAR)

if __name__ == '__main__':
    l = KLex()
    p = KParse()

    while True:
        try:
            text = input('K > ')
            if text[-1]==";":
                text=text[0:-1]
            print("INPUT:\t"+text)
            result = p.parse(l.tokenize(text+"\n"))
            print("RTYPE:\t"+str(type(result)))
            #print("    "+to_source(result))
            for a in result:
                eval(compile(a, filename="<ast>", mode="eval"))
                print("    ==> "+to_source(a)+": "+str(type(eval(compile(a, filename="<ast>", mode="eval"))))+"\n") # FIXME: remove this ridiculous double evaluation!
        except TypeError as e:
            print("TypeError: "+str(e))
        except EOFError:
            break
