import re
import ply.lex as lex

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE'
}

literals = ['.', '=', '+', '-', '*', '/', ',', ':', '#', '|', '"', "'",'(',')']


# Definir a lista de tokens
tokens = [
    'TAG',
    'ID',
    'CLASS',
    'ATTRIBUTE',
    'TEXT',
    'NEWLINE',
    'INDENT',
    'DEDENT',
]

tokens = tokens + list(reserved.values())

last_indent = 0  # variável global para armazenar a indentação da última linha lida

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_NEWLINE(t):
    r'\s+'
    global last_indent
    new_indent = 0
    for c in t.value:
        if c == ' ':
            new_indent += 1
        elif c == '\t':
            new_indent += 4  # assumindo que uma tabulação equivale a 4 espaços
    t.lexer.lineno += t.value.count('\n')  # atualiza o número de linhas lidas
    if new_indent > last_indent:
        t.type = 'INDENT'
        t.value = new_indent - last_indent
        last_indent = new_indent
    elif new_indent < last_indent:
        t.type = 'DEDENT'
        t.value = last_indent - new_indent
        last_indent = new_indent
    else:
        t.type = 'NEWLINE'
        t.value = None
    return t

# Definir as regras para os tokens
def t_TEXT(t):
    r'.+'
    t.type = reserved.get(t.value, 'TEXT')
    return t

# Ignorar espaços em branco
t_ignore = ' \t'

# Tratar erros de caracteres inválidos
def t_error(t):
    print("Caractere inválido '%s'" % t.value[0])
    t.lexer.skip(1)

# Definir a precedência dos operadores
precedence = ()

# Criar o lexer
lexer = lex.lex()

# Testar o lexer
lexer.indent_stack = [0]
data = """
html(lang="en")
    head
        title= pageTitle
        script(type='text/javascript').
            if (foo) bar(1 + 5)
    body
        h1 Pug - node template engine
        #container.col
            if youAreUsingPug
                p You are amazing
            else
                p Get on it!
            p.
                Pug is a terse and simple templating language with a
                strong focus on performance and powerful features
"""

lexer.input(data)
for tok in lexer:
    print(tok)