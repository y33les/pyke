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

    @_('line NEWLINE')
    def root(self,p):
        self.pc+=1
        print(str(self.pc)+":\teN:\t"+astck(p.line))
        self.pc=0 # reset PC ready for next expression
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.line)))
        return self.asts

    @_('expr SEMI line')
    def line(self,p):
        self.pc+=1
        #print
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.line)))
        return p.expr

    @_('paren SEMI line')
    def line(self,p):
        self.pc+=1
        #print
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.line)))
        return p.paren

    @_('expr SEMI expr')
    def line(self,p):
        self.pc+=1
        #print(str(self.pc)+":\te;e:\t"+astck(p.expr))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.expr1)))
        return p.expr0

    @_('expr SEMI paren')
    def line(self,p):
        self.pc+=1
        #print(str(self.pc)+":\te;e:\t"+astck(p.expr))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.paren)))
        return p.expr

    @_('paren SEMI expr')
    def line(self,p):
        self.pc+=1
        #print(str(self.pc)+":\te;e:\t"+astck(p.expr))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.expr)))
        return p.paren

    @_('paren SEMI paren')
    def line(self,p):
        self.pc+=1
        #print(str(self.pc)+":\tp;p:\t"+astck(p.paren))
        self.asts.append(ast.fix_missing_locations(ast.Expression(p.paren1)))
        return self.paren0

    @_('paren SPACE paren')
    def root(self,p):
        self.pc=0
        raise Exception("'typ") # This is what ngn/k does for both `1 (!3)` and `1 (2+3)`

    @_('expr SPACE paren')
    def root(self,p):
        self.pc=0
        raise Exception("'typ") # This is what ngn/k does for both `1 (!3)` and `1 (2+3)`

    @_('paren SPACE expr')
    def root(self,p):
        self.pc=0
        raise Exception("'typ") # This is what ngn/k does for both `1 (!3)` and `1 (2+3)`

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

    @_('value')
    def expr(self,p):
        self.pc+=1
        print(str(self.pc)+":\tv:\t"+astck(p.value))
        return p.value

    @_('tuple')
    def expr(self,p):
        self.pc+=1
        print(str(self.pc)+":\tt:\t"+astck(p.tuple))
        return p.tuple

    @_('atom')
    def value(self,p):
        self.pc+=1
        print(str(self.pc)+":\ta:\t"+astck(p.atom))
        return p.atom

    @_('NUMBER')
    def atom(self,p):
        self.pc+=1
        print(str(self.pc)+":\tn:\t"+astck(ast.Constant(p.NUMBER))+"\tn="+str(p.NUMBER)+"\n")
        return ast.Constant(p.NUMBER)

    @_('CHAR')
    def atom(self,p):
        self.pc+=1
        print(str(self.pc)+":\tc:\t"+astck(ast.Constant(p.CHAR))+"\tc="+p.CHAR+"\n")
        return ast.Constant(p.CHAR)

    @_('QUIT NEWLINE')
    def root(self,p):
        exit(0)

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
