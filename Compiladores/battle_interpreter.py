import random

class Character:
    def __init__(self, nome, vida=100, mana=100):
        self.nome = nome
        self.vida = vida
        self.mana = mana
        self.defesa_ativa = None

    def esta_vivo(self):
        return self.vida > 0
    
class DefenseState:
    def __init__(self, tipo, valor):
        self.tipo = tipo      # 'escudo', 'desviar', 'cura'
        self.valor = valor    # % redução, chance, cura



class GameState:
    def __init__(self):
        self.attacks = {
            "soco": {
                "dano": 10,
                "mana": 0
            },
            "fogo": {
                "dano": 30,
                "mana": 20
            },
            "tiro": {
                "dano": 25,
                "mana": 15
            }
        }

        self.player = Character("Jogador")
        self.bot = Character("Bot")

        self.game_over = False

    
class BattleInterpreter:

    def __init__(self):
        self.state = GameState()

    def execute(self, ast):
        command = ast[0]

        if command == "CONVOCAR":
            return self._convocar(ast[1])

        elif command == "APRENDER":
            return self._aprender(ast[1])

        elif command == "ATACAR":
            return self._atacar(ast[1], ast[2])

        elif command == "DEFENDER":
            return self._defender(ast[1])

        elif command == "HELP":
            return self._help(ast[0])
        else:
            raise Exception(f"Comando desconhecido: {command}")

    # =========================
    # Comandos
    # =========================

    def _convocar(self, entity):
        self.state.character = entity
        return f"{entity.capitalize()} foi convocado!"

    def _aprender(self, attack_data):
        nome = attack_data.get("nome_ataque")
        dano = attack_data.get("dano")
        mana = attack_data.get("mana")

        if not nome or dano is None or mana is None:
            raise Exception("Ataque inválido: nome_ataque, dano e mana são obrigatórios")
        
        if nome in self.state.attacks:
         raise Exception("Ataque já existe")

        self.state.attacks[nome] = {
            "dano": dano,
            "mana": mana
        }

        print (f"\nAtaque '{nome}' aprendido (dano={dano}, mana={mana})")
        self._bot_turn()

    def _atacar(self, ataque_nome, parte):
        if self.state.game_over:
            print("O jogo acabou.")
            return

        attacks = self.state.attacks

        if ataque_nome not in attacks:
            raise Exception(f"\nAtaque '{ataque_nome}' não existe")

        ataque = attacks[ataque_nome]
        jogador = self.state.player
        bot = self.state.bot

        # checa mana
        if jogador.mana < ataque["mana"]:
            print("\nMana insuficiente!")
            return

        # aplica ataque
        jogador.mana -= ataque["mana"]
        bot.vida -= ataque["dano"]

        print(
            f"\n{jogador.nome} atacou o {bot.nome} "
            f"na {parte} com {ataque_nome} "
            f"(dano={ataque['dano']})"
        )

        self._status()

        if not bot.esta_vivo():
            print("\nO BOT MORREU! VOCÊ VENCEU!")
            self.state.game_over = True
            return

        self._bot_turn()


    def _defender(self, defense_type):
        print(f"\nDefesa ativada: {defense_type.upper()}") 
        self._bot_turn()
    

    def _bot_turn(self):

        bot = self.state.bot
        jogador = self.state.player

        ataque_nome, ataque = random.choice(list(self.state.attacks.items()))

        if bot.mana < ataque["mana"]:
            print("Bot tentou atacar, mas sem mana")
            return

        bot.mana -= ataque["mana"]

        dano = ataque["dano"]

        
        defesa = jogador.defesa_ativa

        if defesa:
            if defesa.tipo == "escudo":
                dano = int(dano * (1 - defesa.valor))
                print("🛡️ Escudo reduziu o dano!")

            elif defesa.tipo == "desviar":
                if random.random() < defesa.valor:
                    dano = 0
                    print("💨 Ataque desviado!")

            jogador.defesa_ativa = None  # defesa consumida

        jogador.vida -= dano

        print(
            f"\n Bot atacou com {ataque_nome} "
            f"(dano={dano})"
        )

        self._status()

        if not jogador.esta_vivo():
            print("VOCÊ MORREU!")
            self.state.game_over = True


            self._status()

            if not jogador.esta_vivo():
                print("VOCÊ MORREU! GAME OVER.")
                self.state.game_over = True

    def _status(self):
        p = self.state.player
        b = self.state.bot

        print(
            f"STATUS → "
            f"Jogador: HP={p.vida}, Mana={p.mana} | "
            f"Bot: HP={b.vida}, Mana={b.mana}"
        )


    def _defender(self, defesa_nome):
        DEFESAS = {
        "escudo": {"tipo": "escudo", "valor": 0.5, "mana": 20},
        "desviar": {"tipo": "desviar", "valor": 0.3, "mana": 15},
        "cura": {"tipo": "cura", "valor": 25, "mana": 20},
        }
        jogador = self.state.player

        if defesa_nome not in DEFESAS:
            raise Exception("Defesa desconhecida")

        defesa = DEFESAS[defesa_nome]

        if jogador.mana < defesa["mana"]:
            print("\nMana insuficiente para defender")
            return

        jogador.mana -= defesa["mana"]

        # cura é imediata
        if defesa["tipo"] == "cura":
            jogador.vida += defesa["valor"]
            if jogador.vida > 100:
                jogador.vida = 100
            print(f"\n{jogador.nome} usou Cura (+{defesa['valor']} HP)")
            self._status()
            self._bot_turn()
            return

        # escudo ou desviar
        jogador.defesa_ativa = DefenseState(
            defesa["tipo"],
            defesa["valor"]
        )

        print(f"\n{jogador.nome} ativou defesa: {defesa_nome}")
        self._bot_turn()

    def _help(self, data):
        help_text = """
        Comandos disponíveis:

        1. CONVOCAR [personagem]:
           - Convoca um personagem para a batalha.
           - Exemplo: CONVOCAR Guerreiro

        2. APRENDER [nome_ataque] [dano] [mana]:
           - Aprende um novo ataque, fornecendo o nome, dano e mana.
           - Exemplo: APRENDER soco 10 0

        3. ATACAR [nome_ataque] NA [parte_do_corpo]:
           - Realiza um ataque usando um ataque previamente aprendido.
           - Exemplo: ATACAR fogo NA Barriga

        4. DEFENDER [nome_defesa]:
           - Usa uma defesa. A defesa pode ser uma ação como 'Cura'.
           - Exemplo: DEFENDER Cura

        5. HELP:
           - Exibe esta ajuda com os comandos disponíveis e suas explicações.

        Ataques disponíveis:
        """
        for idx, (name, attack) in enumerate(self.state.attacks.items(), 1):
            help_text += f"T: Ataque {idx}: {name.capitalize()} - Dano: {attack['dano']}, Mana: {attack['mana']}\n"

        help_text += "\nExemplo de uso: ATACAR [nome_ataque]"

        return help_text

