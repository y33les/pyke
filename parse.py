from sly import Parser
from lex import KLex

class KParse(Parser):
    tokens = KLex.tokens

    @_('expr PLUS term')
    def expr(self,p):
        return p.expr + p.term

    @_('term')
    def expr(self,p):
        return p.term

    @_('factor')
    def term(self,p):
        return p.factor

    @_('NUMBER')
    def factor(self,p):
        return p.NUMBER

if __name__ == '__main__':
    l = KLex()
    p = KParse()

    while True:
        try:
            t = input('  ')
            r = p.parse(l.tokenize(t))
            print(r)
        except EOFError:
            break
