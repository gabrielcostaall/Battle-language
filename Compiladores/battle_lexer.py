from sly import Lexer

class BattleLexer(Lexer):

    tokens = {
        CONVOCAR, ATACAR, DEFENDER,
        GUERREIRO, ARQUEIRO, MAGO,
        CURA, ESCUDO, ESQUIVAR,
        BARRIGA, CABECA, PERNA,
        NA, APRENDER, IDENT, NUMBER, 
        STRING, COLON, COMMA
    }

    ignore = ' \t'
    ignore_newline = r'\n+'

    #Ações
    CONVOCAR = r'CONVOCAR'
    ATACAR   = r'ATACAR'
    DEFENDER = r'DEFENDER'
    APRENDER = r'APRENDER'

    # Entidades
    GUERREIRO = r'Guerreiro'
    ARQUEIRO  = r'Arqueiro'
    MAGO      = r'Mago'

    # Defesas
    CURA    = r'Cura'
    ESCUDO  = r'Escudo'
    ESQUIVAR = r'Esquivar'

    # Partes do corpo
    BARRIGA = r'Barriga'
    CABECA  = r'Cabeça'
    PERNA   = r'Perna'

    # Palavras auxiliares
    NA = r'NA'
    COLON = r':'
    COMMA = r','

    literals = { '(', ')' }

    IDENT  = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    STRING = r'"[^"]*"'