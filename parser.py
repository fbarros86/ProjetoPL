import ply.yacc as yacc
import re
from lex import tokens,literals

"""
pug : conteudo

conteudo : conteudo elem
         | elem
         
elem : TAG tagProperties TEXT INDENT conteudo DEDENT
     | TAG tagProperties TEXT INDENT conteudo
     | TAG TEXT INDENT conteudo DEDENT
     | TAG TEXT INDENT conteudo
     | TAG tagProperties INDENT conteudo DEDENT
     | TAG tagProperties INDENT conteudo
     | TAG tagProperties EQUALS VALUE INDENT conteudo DEDENT
     | TAG tagProperties EQUALS VALUE INDENT conteudo
     | TAG INDENT conteudo DEDENT
     | TAG INDENT conteudo
     | TAG EQUALS VALUE INDENT conteudo DEDENT
     | TAG EQUALS VALUE INDENT conteudo
     | TAG tagProperties POINT  linhasTexto DEDENT
     | TAG tagProperties POINT  linhasTexto
     | TAG POINT linhasTexto DEDENT
     | TAG POINT linhasTexto
     | TAG tagProperties TEXT
     | TAG TEXT
     | TAG tagProperties
     | TAG
     | TAG tagProperties EQUALS VALUE
     | TAG EQUALS VALUE
     | INCLUDE TEXT
     | IF CONDITION INDENT conteudo DEDENT ELSE INDENT conteudo DEDENT
     | IF CONDITION INDENT conteudo DEDENT ELSE INDENT conteudo 
     | IF CONDITION INDENT conteudo DEDENT elsesif ELSE INDENT conteudo DEDENT
     | IF CONDITION INDENT conteudo DEDENT elsesif ELSE INDENT conteudo
     | IF CONDITION INDENT conteudo DEDENT elsesif
     | IF CONDITION INDENT conteudo DEDENT
     | IF CONDITION INDENT conteudo
     | UNLESS CONDITION INDENT conteudo DEDENT 
     | UNLESS CONDITION INDENT conteudo 
     | LINECOMMENT
     | BLOCKCOMMENT listaComments DEDENT
     | BLOCKCOMMENT listaComments
     | POINT TEXT
     | WHILE CONDITION INDENT conteudo DEDENT
     | WHILE CONDITION INDENT conteudo 
     | EACH VALUE IN iterable INDENT conteudo DEDENT
     | EACH VALUE IN iterable INDENT conteudo 
     | pipedText
     | JS VAR TEXT "=" elemIterable
     
elsesif : elsesif ELSE IF CONDITION INDENT conteudo DEDENT
        | elsesif ELSE IF CONDITION INDENT conteudo
        | ELSE IF CONDITION INDENT conteudo DEDENT
        | ELSE IF CONDITION INDENT conteudo
        
pipedText : PIPED TEXT
          | pipedText PIPED TEXT
          
iterable : '[' elemsLista ']'
         | '{' elemsLista '}'
         | '{' elemsDict '}'
         
elemsLista : elemIterable
           | elemsLista ',' elemIterable 
           
elemsDict : elemIterable ':' elemIterable
          | elemsDict ',' elemIterable ':' elemIterable
          
elemIterable : STRING
             | NUMBER
             
listaComments : COMMENT
              | listaComments COMMENT
              
tagProperties : ID
              | listaClasses
              | PA ATTRIBUTE PF
              | ID PA ATTRIBUTE PF
              | ID listaClasses
              | ID listaClasses PA ATTRIBUTE PF
              | listaClasses PA ATTRIBUTE PF
              
listaClasses : CLASS
             | listaClasses CLASS
             
linhasTexto : linhasTexto TEXT
            | TEXT
"""

variaveis = {}

def p_pug(p):
    'pug : conteudo'
    p[0]=p[1]

def p_conteudo(p):
    'conteudo : conteudo elem'
    p[0]=p[1]+p[2]

def p_conteudo_vazio(p):
    'conteudo : elem'
    p[0]=p[1]
    
    
    
    
def p_elem_todo(p):
    '''elem : TAG tagProperties TEXT INDENT conteudo DEDENT
            | TAG tagProperties TEXT INDENT conteudo'''
    p[0] = f"<{p[1]} {p[2]}>{p[3]}\n{p[5]}</{p[1]}>\n"

def p_elem_semProps(p):
    '''elem : TAG TEXT INDENT conteudo DEDENT
            | TAG TEXT INDENT conteudo'''
    p[0] = f"<{p[1]} >{p[2]}\n{p[4]}</{p[1]}>\n"
    

def p_elem_sem_text(p):
    '''elem : TAG tagProperties INDENT conteudo DEDENT
            | TAG tagProperties INDENT conteudo'''
    p[0] = f"<{p[1]} {p[2]}>\n{p[4]}</{p[1]}>\n"

def p_elem_var(p):
    '''elem : TAG tagProperties EQUALS VALUE INDENT conteudo DEDENT
            | TAG tagProperties EQUALS VALUE INDENT conteudo'''
    flag=0
    for key,value in variaveis.items():
        if re.search(key,p[4]):
            p[4]=re.sub(key,value,p[4])
            flag=1
            break
    if flag: p[0] = f"<{p[1]} {p[2]}>{p[4]}\n{p[6]}</{p[1]}>\n"
    else: raise Exception(f"Variable not found: {p[4]}")
    
def p_elem_sem_text_props(p):
    '''elem : TAG INDENT conteudo DEDENT
            | TAG INDENT conteudo'''
    p[0] = f"<{p[1]}>\n{p[3]}</{p[1]}>\n"

def p_elem_sem_props_var(p):
    '''elem : TAG EQUALS VALUE INDENT conteudo DEDENT
            | TAG EQUALS VALUE INDENT conteudo'''
    flag=0
    for key,value in variaveis.items():
        if re.search(key,p[3]):
            p[3]=re.sub(key,value,p[3])
            flag=1
            break
    if flag: p[0] = f"<{p[1]}>{p[3]}\n{p[5]}</{p[1]}>\n"
    else: raise Exception(f"Variable not found: {p[3]}")
    
def p_elem_sem_text_point(p):
    '''elem : TAG tagProperties POINT  linhasTexto DEDENT
            | TAG tagProperties POINT  linhasTexto'''
    p[0] = f"<{p[1]} {p[2]}>{p[4]}</{p[1]}>\n"


def p_elem_sem_text_props_point(p):
    '''elem : TAG POINT   linhasTexto DEDENT
            | TAG POINT  linhasTexto'''
    p[0] = f"<{p[1]}>{p[3]}</{p[1]}>\n"

def p_elem_linha(p):
    'elem : TAG tagProperties TEXT'
    p[0] = f"<{p[1]} {p[2]}>{p[3]}</{p[1]}>\n"

def p_elem_linha_sem_props(p):
    'elem : TAG TEXT'
    if (p[1]=="doctype"): p[0]=f"<!DOCTYPE {p[2]}>\n"
    else: p[0] = f"<{p[1]} >{p[2]}</{p[1]}>\n"

def p_elem_linha_sem_text(p):
    'elem : TAG tagProperties'
    p[0] = f"<{p[1]} {p[2]}/>\n"

def p_elem_linha_sem_text_props(p):
    'elem : TAG'
    p[0] = f"<{p[1]}/>\n"

def p_elem_linha_var(p):
    'elem : TAG tagProperties EQUALS VALUE'
    flag=0
    for key,value in variaveis.items():
        if re.search(key,p[4]):
            p[4]=re.sub(key,value,p[4])
            flag=1
            break
    if flag: p[0] = f"<{p[1]}  {p[2]}>{p[4]}</{p[1]}>\n"
    else: raise Exception(f"Variable not found: {p[4]}")

def p_elem_linha_sem_props_var(p):
    'elem : TAG EQUALS VALUE'
    flag=0
    for key,value in variaveis.items():
        if re.search(key,p[3]):
            p[3]=re.sub(key,value,p[3])
            flag=1
            break
    if flag: p[0] = f"<{p[1]}>{p[3]}</{p[1]}>\n"
    else: raise Exception(f"Variable not found: {p[3]}")
    

def p_elem_include(p):
    'elem : INCLUDE TEXT'
    #adicionar para ficheiros pug
    with open(p[2]) as f:
        p[0]=f.read()+"\n"
    

def p_elem_if_else_condition(p):
    '''elem : IF CONDITION INDENT conteudo DEDENT ELSE INDENT conteudo DEDENT
            | IF CONDITION INDENT conteudo DEDENT ELSE INDENT conteudo
    '''
    for key,value in variaveis.items():
        if re.search(key,p[2]):
            p[2]=re.sub(key,value,p[2])
    if(eval(p[2])):
        p[0]=p[4]
    else:
        p[0] = p[8]

def p_elem_elseif_condition(p):
    '''elem : IF CONDITION INDENT conteudo DEDENT elsesif ELSE INDENT conteudo DEDENT
            | IF CONDITION INDENT conteudo DEDENT elsesif ELSE INDENT conteudo
            | IF CONDITION INDENT conteudo DEDENT elsesif'''
    for key,value in variaveis.items():
        if re.search(key,p[2]):
            p[2]=re.sub(key,value,p[2])
    if(eval(p[2])): p[0]=p[4]
    elif(p[6][0]==1): p[0]=p[6][1]
    elif(p[6][0]==-1): raise Exception(p[6][1])
    elif(len(p)>=10): p[0] = p[9]
    else:p[0]=""

def p_elesif(p):
    '''elsesif : elsesif ELSE IF CONDITION INDENT conteudo DEDENT
               | elsesif ELSE IF CONDITION INDENT conteudo
               | ELSE IF CONDITION INDENT conteudo DEDENT
               | ELSE IF CONDITION INDENT conteudo'''
    p[0]=None
    try:
        if len(p)==8:
                if p[1][0]==1: p[0]=p[1]
                elif p[1][0]==-1:  p[0]=(-1,e)
                else:
                    for key,value in variaveis.items():
                        if re.search(key,p[4]):  p[4]=re.sub(key,value,p[4])
                    if eval(p[4]): p[0]=(1,p[6])
                    else: p[0]=(0,0)

        else:
            for key,value in variaveis.items():
                if re.search(key,p[3]): p[3]=re.sub(key,value,p[3])
            if eval(p[3]): p[0]=(1,p[5])
            else: p[0]=(0,0)
    except Exception as e:
        p[0]=(-1,e)
        

def p_elem_if_condition(p):
    '''elem : IF CONDITION INDENT conteudo DEDENT
            | IF CONDITION INDENT conteudo'''
    for key,value in variaveis.items():
        if re.search(key,p[2]):
            p[2]=re.sub(key,value,p[2])
    if(eval(p[2])):
        p[0]=p[4]
    else: p[0] =""

def p_elem_unless_condition(p):
    '''elem : UNLESS CONDITION INDENT conteudo DEDENT
            | UNLESS CONDITION INDENT conteudo'''
    for key,value in variaveis.items():
        if re.search(key,p[2]):
             p[2]=re.sub(key,value,p[2])
    if(not eval(p[2])):
        p[0]=p[4]
    else: p[0] =""

def p_elem_line_comment(p):
    'elem : LINECOMMENT'
    p[0] = f"<!--{p[1][2:]}-->\n"

def p_elem_line_blockcomment(p):
    '''elem : BLOCKCOMMENT listaComments DEDENT
            | BLOCKCOMMENT listaComments'''
    p[0] = f"<!--{p[2]}-->\n"

def p_elem_text(p):
    'elem : POINT TEXT'
    p[0] = p[2]


def p_elem_while(p):
    '''elem : WHILE CONDITION INDENT conteudo DEDENT
            | WHILE CONDITION INDENT conteudo'''
    p[0]=""
    for key,value in variaveis.items():
        if re.search(key,p[2]):
             p[2]=re.sub(key,value,p[2])
    while eval(p[2]):
        p[0]+=p[4]

def p_elem_each_in(p):
    '''elem : EACH VALUE IN iterable INDENT conteudo DEDENT
            | EACH VALUE IN iterable INDENT conteudo'''
    p[0]=""
    for p[2] in p[4]:
        p[0]+=p[6]

def p_elem_piped(p):
    'elem : pipedText'
    p[0]=p[1]

def p_pipedText(p):
    '''pipedText : PIPED TEXT
                 | pipedText PIPED TEXT   '''
    if (len(p)==3): p[0]=p[2]
    else: p[0]=p[1]+"\n"+p[3]

def p_iterable_lista(p):
    """iterable : '[' elemsLista ']'"""
    p[0]=p[2]

def p_iterable_set(p):
    """iterable : '{' elemsLista '}'"""
    p[0]=set(p[2])

def p_iterable_dict(p):
    """iterable : '{' elemsDict '}'"""
    p[0]=p[2]
    
def p_elemsLista(p):
    ''' elemsLista : elemIterable
                    | elemsLista ',' elemIterable 
    '''   
    if len(p)==2: p[0]=[p[1]]
    else: p[0]=p[1]+[p[3]]

def p_elemsDict(p):
    ''' elemsDict : elemIterable ':' elemIterable
                    | elemsDict ',' elemIterable ':' elemIterable
    '''   
    if len(p)==4: p[0]={p[1]:p[3]}
    else:
        p[0]=p[1]
        p[0][p[3]]=p[5]
        
def p_elemIterable(p):
    """ elemIterable : STRING
                    | NUMBER"""
    p[0]=p[1]

def p_listaComments(p):
    '''listaComments : COMMENT
                    | listaComments COMMENT'''
    if len(p)==2: p[0]=p[1]
    else: p[0]=p[1]+"\n"+p[2]
    
def p_elem_javascript(p):
    'elem : JS VAR TEXT "=" elemIterable'
    variaveis[p[3].strip()]=p[5]
    p[0]=""


def p_tagProperties_id(p):
    "tagProperties : ID"
    p[0]=f"\"{p[1]}\""



def p_tagProperties_class(p):
    "tagProperties : listaClasses"
    p[0]=f"class={p[1]}"

def p_tagProperties_attributes(p):
    "tagProperties : PA ATTRIBUTE PF"
    p[0]=" "
    for attr in p[2]:
        p[0]+=attr+" "

def p_tagProperties_sem_class(p):
    "tagProperties : ID  PA ATTRIBUTE PF"
    p[0]=f'id="{p[1]}" '
    for attr in p[3]:
        p[0]+=attr+" "

def p_tagProperties_sem_attrib(p):
    "tagProperties : ID listaClasses"
    p[0]=f'id="{p[1]}" class={p[2]} '

def p_tagProperties(p):
    "tagProperties : ID listaClasses PA ATTRIBUTE PF"
    p[0]=f'id="{p[1]}" class={p[2]} '
    for attr in p[4]:
        p[0]+=attr+" "

def p_tagProperties_sem_id(p):
    "tagProperties : listaClasses PA ATTRIBUTE PF"
    p[0]=f"class={p[1]} "
    for attr in p[3]:
        p[0]+=attr+" "

def p_listaClasses(p):
    """listaClasses : CLASS
                    | listaClasses CLASS"""
    if (len(p)==2):
        if(p[1][0]=='"'): p[0]=f'{p[1]}'
        else: p[0]=f'"{p[1]}"'
    else: p[0]=f'"{p[1][1:-1]} {p[2]}"'

def p_linhasTexto(p):
    """
    linhasTexto : linhasTexto TEXT
                | TEXT
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "\n" + p[2]


def p_error(p):
    print("Erro sintático", p)


parser = yacc.yacc()
with open("test1.pug") as f:
    data = f.read()
result = parser.parse(data)
with open("test.html","w") as f:
    f.write(result)

