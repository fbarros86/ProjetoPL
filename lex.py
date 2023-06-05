import re
import ply.lex as lex

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'unless' : 'UNLESS',
   'each':'EACH',
   'in':'IN',
   'include':'INCLUDE'
}

literals = [',', ':','[',']','{','}','=']

# Definir a lista de tokens
tokens = [
    'POINT',
    'PA',
    'PF',
    'EQUALS',
    'TAG',
    'ID',
    'CLASS',
    'ATTRIBUTE',
    'TEXT',
    'INDENT',
    'DEDENT',
    'CONDITION',
    'LINECOMMENT',
    'BLOCKCOMMENT',
    'PIPED',
    'VALUE',
    'COMMENT',
    'NUMBER',
    'STRING',
    'JS',
    'VAR'
] + list(reserved.values())

states = (
    ('comment', 'exclusive'),
    ('pointState', 'exclusive'),
    ('conditional', 'exclusive'),
    ('each', 'exclusive'),
    ('firstWord', 'inclusive'),
    ('ignoreComments', 'exclusive'),
    ('js','exclusive'),
    ('dedent','exclusive'),
    ('indent','exclusive')
)

indent_level = 0
indent = 0
dedent=0

def t_PA(t):    
    r'\('
    return t

def t_ATTRIBUTE(t):
    r'(?<=\()\n?(.|\n)+?\n?(?=\))'
    if '\n' in t.value:
        attr_list = re.split(r'\n', t.value)
        attr_list=attr_list[1:-1]
    else:
        attr_list = re.split(r',', t.value)
    attrs = []
    for attr in attr_list:
        attrs.append(attr.strip())
    t.value = attrs
    return t

def t_VALUE(t):
    r'(?<=\=\s)[\w\+\-\*\/]*'
    return t

def t_POINT(t):
    r'\.'
    if t.lexer.current_state() == "firstWord":
        t.type = "TAG"
        t.value = "div"  
        t.lexer.pop_state()
    elif t.lexer.lexdata[t.lexer.lexpos] == '\n':
        t.lexer.push_state('pointState')
    else:
        t = None
    return t

def t_HASHTAG(t):
    r'\#'
    if t.lexer.current_state() == "firstWord":
        t.type = "TAG"
        t.value = "div"  
        t.lexer.pop_state()
    else:
        t = None
    return t

def t_PF(t):
    r'\)'
    return t

def t_EQUALS(t):
    r'\='
    return t

def t_CLASS(t):
    r'(?<=\.)[^\.\s\(\#]+'
    return t

def t_BLOCKCOMMENT(t):
    r'//\s*(?=\n)'
    t.lexer.push_state('comment')
    return t    

def t_IGNORE_BLOCKCOMMENT(t):
    r'//\-\s*(?=\n)'
    t.lexer.push_state('ignoreComments')
    pass

def t_IGNORE_LINECOMMENT(t):
    r'//\-.*'
    pass

def t_LINECOMMENT(t):
    r'//.*'
    return t

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global first_word, indent_level, indent,dedent
    next_indent_level = 0
    if t.lexer.current_state() == "each":
        t.lexer.pop_state()
    if t.lexer.current_state() == "INITIAL":
        t.lexer.push_state('firstWord')

    # Contar o número de espaços e tabulações no início da próxima linha
    line = t.lexer.lexdata[t.lexer.lexpos:]
    if (not re.match(r"[ \t]*\n",line)): 
        next_indent_level = len(line) - len(line.lstrip(' ')) + (len(line) - len(line.lstrip('\t'))) * 4
        if next_indent_level > indent_level:
            if t.lexer.current_state() == "firstWord" :
                    indent=(next_indent_level - indent_level)/4
                    t.lexer.push_state("indent")
        elif next_indent_level < indent_level:
            if t.lexer.current_state() == "ignoreComments":
                t.lexer.pop_state()
            else :
                dedent=(indent_level - next_indent_level)/4
                t.lexer.push_state("dedent")
        else:
            if t.lexer.current_state() == 'js':
                    t.lexer.pop_state()
                    t.lexer.push_state('firstWord')
        indent_level = next_indent_level

    
def t_indent_INDENT(t):
    r'(.|\n)'
    global indent
    t.lexer.lexpos -= 1
    if indent>0:
        indent-=1
        t.value=""
        return t
    else:
        t.lexer.pop_state()
        
    

def t_dedent_DEDENT(t):
    r'(.|\n)'
    global dedent
    t.lexer.lexpos -= 1
    if dedent>0:
        dedent-=1
        t.value=""
        return t
    else:
        t.lexer.pop_state()
        if t.lexer.current_state() != 'INITIAL':
                        t.lexer.pop_state()
                        t.lexer.push_state("firstWord")    


def t_ID(t):
    r'(?<=\#)[a-zA-Z_-][a-zA-Z\d_-]*'
    return t


def t_conditional_CONDITION(t):
    r'.+'
    t.lexer.pop_state()
    return t

def t_comment_pointStare_ignoreComments_CONTENT(t):
    r'.+'
    if t.lexer.current_state() == "comment":
        t.type = 'COMMENT' 
    if t.lexer.current_state() == "pointState":
        t.type = 'TEXT'          
    return t

def t_firstWord_PIPED(t):
    r"\|"
    t.lexer.pop_state()
    return t
    

def t_firstWord_TAG(t):
    r'[a-z]\w*\/?'
    t.type = reserved.get(t.value, 'TAG')
    if(t.type!="ELSE"): t.lexer.pop_state()
    if t.type=="IF" or t.type=="UNLESS" or t.type=="WHILE":
        t.lexer.push_state("conditional")
    if(t.type=="EACH"): t.lexer.push_state("each")
    return t

def t_firstWord_JS(t):
    r'-'
    t.lexer.pop_state()
    t.lexer.push_state('js')
    return t

def t_js_VAR(t):
    r'\bvar\b'
    return t

def t_js_NUMBER(t):
    r'\b-?\d+(\.\d+)?\b'
    return t

def t_js_STRING(t):
    r'(\"|\').+?(\"|\')'
    t.value=  t.value[1:-1]
    return t

def t_js_TEXT(t):
    r'[\w ]+'
    return t
    

def t_each_VALUE(t):
    r'.+?(?=in)'
    return t

def t_each_IN(t):
    r'in'
    return t

def t_each_NUMBER(t):
    r'-?\d+(\.\d+)?'
    return t

def t_each_STRING(t):
    r'(\"|\').+?(\"|\')'
    t.value=  t.value[1:-1]
    return t

 


def t_TEXT(t):
    r'.+'
    t.type = reserved.get(t.value, 'TEXT')
    return t

def t_pointState_TEXT(t):
    r'.+'
    t.type = reserved.get(t.value, 'TEXT')
    return t

def t_ignoreComments_TEXT(t):
    r'.+'
    pass

t_ANY_ignore = ' \t'

def t_ANY_error(t):
    print("Invalid character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

lexer.indent_stack = [0]
lexer.push_state("firstWord")


            
