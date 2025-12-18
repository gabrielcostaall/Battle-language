from battle_lexer import BattleLexer
from battle_parser import BattleParser
from battle_interpreter import BattleInterpreter

lexer = BattleLexer()
parser = BattleParser()
interpreter = BattleInterpreter()

def run(command):
    ast = parser.parse(lexer.tokenize(command))
    result = interpreter.execute(ast)
    print(result)

command = 0

while command != 1:
    print("\nDigite seu comando (Se quiser parar, digite 1): ")
    command = input()
    if command!="1":
        run (command)
    else:
        print("\n Luta finalizada!")



# run ("CONVOCAR Guerreiro")
# run ('APRENDER (nome_ataque: "tiro", dano: 30, mana: 50)')
# run ("DEFENDER Cura")
# run ("ATACAR tiro NA Barriga")

# lexer = BattleLexer()

# for tok in lexer.tokenize("ATACAR tiro NA Barriga"):
#     print(tok.type, tok.value)
