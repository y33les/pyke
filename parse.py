import ast
from astor import to_source
from sly import Parser
from lex import KLex

class KParse(Parser):
    tokens = KLex.tokens

    @_('expr SEMI')
    def root(self,p):
        return ast.fix_missing_locations(ast.Expression(p.expr))

    @_('expr SPACE expr')
    def array(self,p): # FIXME
        e0 = [p.expr0.elts] if isinstance(p.expr0,ast.List) else [p.expr0]
        e1 = [p.expr1.elts] if isinstance(p.expr1,ast.List) else [p.expr1]
        return ast.List(elts=e0 + e1,ctx=ast.Load())

    @_('LPAREN expr RPAREN')
    def expr(self,p):
        return p.expr

    @_('array')
    def expr(self,p):
        return p.array

    @_('atom')
    def expr(self,p):
        return p.atom

    @_('array SPACE array')
    def array(self,p):
        return ast.List(elts=(p.array0.elts + p.array1.elts),ctx=ast.Load())

    @_('atom SPACE array')
    def array(self,p):
        return ast.List(elts=([p.atom] + p.array.elts),ctx=ast.Load())

    @_('array SPACE atom')
    def array(self,p):
        return ast.List(elts=(p.array.elts + [p.atom]),ctx=ast.Load())

    @_('atom SPACE atom')
    def array(self,p):
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
