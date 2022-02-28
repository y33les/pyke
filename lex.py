from sly import Lexer

class KLex(Lexer):
    # K base verbs: +-*%|&^!<>=~@?_,#$.:
    # K I/O verbs: I/O Verbs 0: 1: 2: 3: 4: 5: 6:
    # K base adverbs: / \ ' /: \: ':
    tokens = { NAME, NUMBER, FLOAT, SYMBOL, CHARACTER, WSPACE,    # Datatypes
               PLUS, MINUS, STAR, PERCENT, PIPE, AMPERSAND, CARET, # Verbs
               BANG, LTHAN, GTHAN, EQUALS, TILDE, AT, QUESTION,
               UNDERSCORE, COMMA, HASH, DOLLAR, DOT, COLON, SPACE,
               FSLASH, BSLASH, TICK, FSCOL, BSCOL, TICKCOL,        # Adverbs
               SCOLON, NEWLINE, BRACKL, BRACKR, SBRACKL, SBRACKR,  # Other
               BRACEL, BRACER }

    ignore_comment_line = r'^\/.*$'
    ignore_comment_inline = r'\s+\/.*$'

    # ignore = r'$\s+' # Ignore leading whitespace # TODO: This + trailing

    # Tokens
    NAME = r'[a-zA-Z][a-zA-Z0-9]*' # TODO: Escape dots?
    SYMBOL = r'`"?[a-zA-Z][a-zA-Z0-9]"?' # TODO: Ensure 2 or no quotes
    CHARACTER = r'".*"' # TODO: Ensure 2 or no quotes - probably better as a rule rather than in this regexp
    WSPACE = r'\s+'
    V=r'([-:+*%!&|<>=~,^#_$?@.]|0:|1:)'
    A=r'(\':|/:|\\:|[\\\'/])'
    N=r'`?"?[a-zA-z][a-zA-Z0-9*]"?'

    # Other
    SCOLON = r';'
    NEWLINE = r'\n'
    BRACKL = r'\('
    BRACKR = r'\)'
    SBRACKL = r'\['
    SBRACKR = r'\]'
    BRACEL = r'\{'
    BRACER = r'\}'

    @_(r'\d*\.?\d+') # TODO: E notation? 0x? 0b? negs not needed as handled by monadic -:
    def NUMBER(self,t):
        try:
            float(t.value)
            return t
        except:
            int(t.value)
            return t

if __name__ == '__main__':
    d = 'x:2;foo:3.45;x+foo /this is a comment' # test with inline comment
    c = '/this is another comment'              # test with line comment
    l = KLex()
    for t in l.tokenize(d):
        print('type=%r, value=%r' % (t.type, t.value))
