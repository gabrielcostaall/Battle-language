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
print("\nLuta iniciada! Caso queira instruções, digite HELP!")

while command != 1:
    print("\nDigite seu comando (Se quiser parar, digite 1): ")
    command = input()
    if command!="1":
        run (command)
    else:
        print("\n Luta finalizada!")

