from sly import Lexer

class KLex(Lexer):
    # K base verbs: +-*%|&^!<>=~@?_,#$.:
    # K I/O verbs: 0: 1: 2: 3: 4: 5: 6:
    # K base adverbs: / \ ' /: \: ':
    tokens = { NUMBER, CHAR, STRING, SYMBOL, ID, PAREN, LBRACK, RBRACK, LBRACE, RBRACE, SPACE, PFUNC, COLON, SEMI, NEWLINE, QUIT }

    # String containing ignored characters between tokens
    ignore_comment_line = r'^\/.*$'
    ignore_comment_inline = r'\s+\/.*$'

    # Regular expression rules for tokens

    @_(r'(m)?\d*\.?\d+(J(m)?\d*\.?\d+)?')  # FIXME: m replaces overbar for ease of testing
    def NUMBER(self,t):
        t.value = t.value.replace('m','-') # FIXME: m replaces overbar for ease of testing
        if 'J' in t.value:
            t.value = t.value.split('J')
            for i in range(len(t.value)):
                if "." in t.value[i]:
                    t.value[i] = float(t.value[i])
                else:
                    t.value[i] = int(t.value[i])
            t.value = complex(t.value[0],t.value[1])
        elif '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t
        # TODO: implement 0x, 0b, E notation - are these already handled by python anyway?

    @_(r'\'.\'')
    def CHAR(self,t):
        t.value=t.value[1:-1]
        return t

    @_(r'\'((\\\')|[^\'(\\\')])+\'')
    def STRING(self,t):
        t.value=t.value[1:-1]
        return t
    # TODO: arrayify into array of CHARs

    @_(r'`\.?[a-zA-Z]+[a-zA-Z0-9\.]*\b')
    def SYMBOL(self,t):
        t.value=t.value[1::]
        return t

    ID      = r'\.?[a-zA-Z]+[a-zA-Z0-9\.]*'
    PAREN  = r'\(.*\)'
    LBRACK = r'\['
    RBRACK = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    SPACE = r'[\ \t]+'
    # TODO: implement characters and strings ("/')

    # K primitive functions
    PFUNC = r'[+\-]'

    # K primitive operators
    # TODO

    # Other K symbols
    COLON = r':'
    SEMI = r';'
    NEWLINE = r'\n'
    QUIT = r'\\\\'

if __name__ == '__main__':
    d = 'x:2;foo:3.45;x+foo;`sym /this is a comment' # test with inline comment
    c = '/this is another comment'              # test with line comment
    l = KLex()
    for t in l.tokenize(d):
        print('type=%r, value=%r' % (t.type, t.value))
