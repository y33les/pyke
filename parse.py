import ast
from astor import to_source
from sly import Parser
from lex import KLex

def I(n):
    return n

def wrap(n):
    return ast.Call(ast.Name(id="I",ctx=ast.Load()),[n],keywords=[])

class KParse(Parser):
    tokens = KLex.tokens
    precedence = (('right',)+tuple(tokens),)
    pd = 0 # Parenthesis depth
    out = []

    @_('expr NEWLINE')
    def root(self,p):
        self.out+=["NL"]
        print(self.out)
        self.out=[]
        return ast.fix_missing_locations(ast.Expression(p.expr))

    @_('expr SPACE expr')
    def list(self,p): # FIXME
        self.out+=["SPACE"]
        return ast.List(elts=[p.expr0,p.expr1],ctx=ast.Load())

#    @_('LPAREN expr RPAREN')
#    def value(self,p):
#        return p.expr
#
#    # TODO: Do we want different cases for ( expr ), ( value ), ( atom ), ( array )?

    @_('LPAREN expr')
    def expr(self,p):
        self.out+=["LPAREN"]
        self.pd-=1
        print("PD: "+str(self.pd))
        if self.pd!=0:
            raise Exception("Unbalanced parentheses!") # FIXME: This doesn't detect pd>0 for some reason
        else:
            return p.expr

    @_('expr RPAREN')
    def expr(self,p):
        self.out+=["RPAREN"]
        self.pd+=1
        print("PD: "+str(self.pd))
        return p.expr

    # TODO: What about e.g. (2);(3), which is legal in ngn/k?
    #       (Note that (2) (3) is not)
    @_('expr SEMI expr')
    def expr(self,p):
        if self.pd<0:
            raise Exception("PD is somehow less than 0")
        elif self.pd==0:
            return ast.Constant("SEMICOLON-SEPARATED EXPRESSIONS!!") # FIXME
        else:
            return ast.List(elts=[(p.expr0.elts if isinstance(p.expr0,ast.List) else [p.expr0])+(p.expr1.elts if isinstance(p.expr1,ast.List) else [p.expr1])],ctx=ast.Load()) # FIXME: this won't work for nested lists, I don't think

    @_('value')
    def expr(self,p):
        return p.value

    @_('list')
    def value(self,p):
        return p.list

    @_('atom')
    def value(self,p):
        self.out+=[str(p.atom.value)]
        return p.atom

#    @_('array SPACE array')
#    def array(self,p):
#        return ast.List(elts=(p.array0.elts + p.array1.elts),ctx=ast.Load())

    @_('atom SPACE list')
    def list(self,p):
        return ast.List(elts=([p.atom] + p.list.elts),ctx=ast.Load())

#    @_('list SPACE atom')
#    def list(self,p):
#        return ast.List(elts=(p.list.elts + [p.atom]),ctx=ast.Load())

    @_('atom SPACE atom')
    def list(self,p):
        return ast.List(elts=[p.atom0,p.atom1],ctx=ast.Load())

    @_('NUMBER')
    def atom(self,p):
        return ast.Constant(p.NUMBER)

    @_('CHAR')
    def atom(self,p):
        if p.CHAR=='q':
            exit(0)
        else:
            return ast.Constant(p.CHAR)

if __name__ == '__main__':
    l = KLex()
    p = KParse()

    while True:
        try:
            text = input('K > ')
            result = p.parse(l.tokenize(text+'\n'))
            print("      "+to_source(result))
            result = eval(compile(result, filename="<ast>", mode="eval"))
            print("      ==> "+str(result)+": "+str(type(result))+"\n")
            #print(result)
        except EOFError:
            break
