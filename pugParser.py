import ply.yacc as yacc
from tokenizer import tokens




"""
Conteudo : linha Conteudo
Conteudo : linha

linha :
"""

def p_conteudo_conteudo(p):
    'conteudo : conteudo linhatoda'
    p[0] = p[1] + p[2]

def p_conteudo_linha(p):
    'conteudo : linhatoda'
    p[0]=p[1]
    
def p_linhatoda_newline(p):
    'linhatoda : linha NEWLINE'
    p[0]=p[1]+"\n"
    
def p_linhatoda_indent(p):
    'linhatoda : linha INDENT'
    p[0]=p[1]+"\n"
    
def p_linhatoda_dedent(p):
    'linhatoda : linha DEDENT'
    p[0]=p[1]+"\n"

def p_linhatoda(p):
    'linhatoda : NEWLINE'
    p[0]="\n"

def p_linha_class_text(p):
    'linha : CLASS TEXT'
    p[0]=f"<div class={p[1]}>{p[2]}"
    
def p_linha_class(p):
    'linha : CLASS'
    p[0]=f"<div class={p[1]}>"
    
def p_linha_class_attribute(p):
    'linha : CLASS ATTRIBUTE'
    p[0]=f"<div class={p[1]} {p[2]}>" #muito aldrabado

def p_linha_class_attribute_text(p):
    'linha : CLASS ATTRIBUTE TEXT'
    p[0]=f"<div class={p[1]} {p[2]}>{p[3]}"

def p_linha_tag(p):
    'linha : TAG'
    p[0]=f"<{p[1]}>"

def p_linha_tag_text(p):
    'linha : TAG TEXT'
    p[0]=f"<{p[1]}>{p[2]}"

def p_linha_tag_attribute(p):
    'linha : TAG ATTRIBUTE'
    p[0]=f"<{p[1]} {p[2]}>"

def p_linha_tag_attribute_text(p):
    'linha : TAG ATTRIBUTE TEXT'
    p[0]=f"<{p[1]} {p[2]}>{p[3]}"

def p_linha_tag_class(p):
    'linha : TAG CLASS'
    p[0]=f"<{p[1]} class={p[2]}>"

def p_linha_tag_class_text(p):
    'linha : TAG CLASS TEXT'
    p[0]=f"<{p[1]} class={p[2]}>{p[3]}"
    
def p_linha_tag_class_attribute(p):
    'linha : TAG CLASS ATTRIBUTE'
    p[0]=f"<{p[1]} class={p[2]} {p[3]}>"
    
def p_linha_tag_class_attribute_text(p):
    'linha : TAG CLASS ATTRIBUTE TEXT'
    p[0]=f"<{p[1]} class={p[2]} {p[3]}>{p[4]}"
  
  
  
  
  
  
  
    
    

def p_error(p):
    print("Erro sintático", p)

data = """
html(lang="en")
    head
        title= pageTitle
        script(type='text/javascript').
    body
        h1 Pug - node template engine
            p.class Pug is a terse and simple templating language with a strong focus on performance and powerful features
"""
parser = yacc.yacc()
result = parser.parse(data)
print(result)