import lex, ast
from re import split

d = 'x:2;foo:3.45;x+foo;`sym /this is a comment' # test with inline comment
c = '/this is another comment'              # test with line comment

class KParse():
    lexer = lex.KLex()
    tokens = lex.KLex.tokens
    token_stream = (None for n in []) # empty generator

    def __init__(self,code):
        self.token_stream = reversed(list(lexer.tokenize(code)))

    def kNum(n:int):
        return ast.Constant(n.value)

    def kChar(c:str):
        if length(c.value) > 1:
            return ast.Tuple(elts=list(map(ast.Constant,c.value)),ctx=ast.Load())
        else:
            return ast.Constant(c.value)

    def kID(i:str):
        return ast.Name(id=i,ctx=ast.Load())

    def cons(e,t:ast.Tuple=ast.Tuple(elts=[],ctx=ast.Load())):
        t.insert(0,e)
        return t

    def parse(phrase):
        for t in self.token_stream:
            out = []
            if t.id=='NEWLINE':
                return out # TODO: turn into ASTs?
            elif t.id=='RPAREN':
                subphrase = []
                tnext = next(self.token_stream)
                while tnext.id!='LPAREN': # TODO: handle semicolons within parens
                    subphrase.append(tnext)
                phrase.append(parse(subphrase)) # FIXME: proper implementation of adding it to the AST
            elif t.id=='NUMBER':
                phrase.insert(0,kNum(t.value))
            elif t.id=='CHAR':
                phrase.insert(0,kChar(t.value))
            elif t.id=='ID':
                phrase.insert(0,kID(t.value))
