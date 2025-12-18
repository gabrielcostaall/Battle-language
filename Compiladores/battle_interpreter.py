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

        self.character = None

    
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

        self.state.attacks[nome] = {
            "dano": dano,
            "mana": mana
        }

        return f"Ataque '{nome}' aprendido (dano={dano}, mana={mana})"

    def _atacar(self, attack_name, body_part):
        if attack_name not in self.state.attacks:
            raise Exception(f"Ataque '{attack_name}' não foi aprendido")

        attack = self.state.attacks[attack_name]

        return (
            f"Ataque {attack_name.upper()} atingiu a {body_part}!\n"
            f"Dano: {attack['dano']} | 🔮 Mana gasta: {attack['mana']}"
        )

    def _defender(self, defense_type):
        return f"Defesa ativada: {defense_type.upper()}"
    
    