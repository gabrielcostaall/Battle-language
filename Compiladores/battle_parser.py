from sly import Parser
from battle_lexer import BattleLexer


class BattleParser(Parser):

    tokens = BattleLexer.tokens

    # Regra inicial
    @_('command')
    def start(self, p):
        return p.command

    # Comandos

    # CONVOCAR <entidade>
    @_('CONVOCAR entity')
    def command(self, p):
        return ("CONVOCAR", p.entity)

    # DEFENDER <defesa>
    @_('DEFENDER defense')
    def command(self, p):
        return ("DEFENDER", p.defense)

    # ATACAR <ataque> NA <parte_corpo>
    @_('ATACAR IDENT NA body_part')
    def command(self, p):
        return ("ATACAR", p.IDENT, p.body_part)

    # Entidades
    @_('GUERREIRO')
    def entity(self, p):
        return "guerreiro"

    @_('ARQUEIRO')
    def entity(self, p):
        return "arqueiro"

    @_('MAGO')
    def entity(self, p):
        return "mago"

    #Aprender
    @_('APRENDER "(" attack_args ")"')
    def command(self, p):
        return ("APRENDER", p.attack_args)


    @_('attack_arg COMMA attack_args')
    def attack_args(self, p):
        return {**p.attack_args, **p.attack_arg}

    @_('attack_arg')
    def attack_args(self, p):
        return p.attack_arg


    @_('IDENT COLON value')
    def attack_arg(self, p):
     return {p.IDENT: p.value}


    @_('NUMBER')
    def value(self, p):
        return int(p.NUMBER)

    @_('STRING')
    def value(self, p):
        return p.STRING.strip('"')
    
    # Tipos de defesa
    @_('CURA')
    def defense(self, p):
        return "cura"

    @_('ESCUDO')
    def defense(self, p):
        return "escudo"

    @_('ESQUIVAR')
    def defense(self, p):
        return "Esquivar"

    # Partes do corpo
    @_('BARRIGA')
    def body_part(self, p):
        return "barriga"

    @_('CABECA')
    def body_part(self, p):
        return "cabeca"

    @_('PERNA')
    def body_part(self, p):
        return "perna"