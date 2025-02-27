from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 1000

class HonestPlayer(BasePokerPlayer):
    def __init__(self,name):
        self.name = name
        self.uuid = None
        self.game_state = {}
        self.show_dowm_hole_cards = []

    def declare_action(self, valid_actions, hole_card, round_state):
        """
        Decide si hacer CALL o FOLD basado en la tasa de victoria estimada.
        """
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )
        self.show_dowm_hole_cards = hole_card
        if win_rate >= 1.0 / self.nb_player:
            action = valid_actions[1]  # CALL
        else:
            action = valid_actions[0]  # FOLD
        
        return action['action'], action['amount']

    def receive_game_start_message(self, game_info):
        """
        Se ejecuta cuando comienza el juego.
        """
        for player in game_info["seats"]:
            if player['name'] == self.name:
                self.uuid = player['uuid']
                break
        print(self.name, self.uuid)
        self.nb_player = game_info['player_num']
        self.game_state["game_info"] = game_info

    def receive_round_start_message(self, round_count, hole_card, seats):
        """
        Se ejecuta al inicio de una nueva ronda.
        """
        self.game_state["hole_card"] = hole_card
        self.game_state["seats"] = seats

    def receive_street_start_message(self, street, round_state):
        """
        Se ejecuta cuando se revela una nueva carta comunitaria.
        """
        self.game_state["community_cards"] = round_state["community_card"]

    def receive_game_update_message(self, action, round_state):
        """
        Se ejecuta cuando un jugador toma una acción en el juego.
        """
        self.game_state["last_action"] = action

    # def receive_round_result_message(self, winners, hand_info, round_state):
    #     """
    #     Muestra las cartas de los jugadores que llegaron al showdown y los ganadores.
    #     """
    #     if "final_hands" not in self.game_state:
    #         self.game_state["final_hands"] = []  # Inicializar solo una vez
    #         print(self.name, " initializing final_hands list")

    #     player_info = {
    #         "name": None,
    #         "cards": [],
    #         "strength": None
    #     }

    #     for player in round_state["seats"]:
    #         if player["state"] in ["participating", "allin"]:  # Solo jugadores en el showdown
    #             if player["uuid"] == self.uuid:
    #                 player_info["name"] = player["name"]
    #                 player_info["cards"] = self.show_dowm_hole_cards  # Guarda las cartas del jugador
    #                 print("Player: ", player["name"], "Cards: ", self.show_dowm_hole_cards)

    #     for info in hand_info:
    #         if info["uuid"] == self.uuid:
    #             player_info["strength"] = info['hand']['hand']['strength']
    #             print("Strength: ", info['hand']['hand']['strength'])

    #     # Añadir la información del jugador a la lista de jugadores activos
    #     self.game_state["final_hands"].append(player_info)

    #     # Guardar los ganadores
    #     self.game_state["winners"] = winners
    def receive_round_result_message(self, winners, hand_info, round_state):
        """
        Guarda las cartas de todos los jugadores activos al finalizar la partida.
        """
        if "final_hands" not in self.game_state:
            self.game_state["final_hands"] = {}  # Inicializa solo una vez

        # Recorremos los jugadores que llegaron al showdown
        for player in round_state["seats"]:
            if player["state"] in ["participating", "allin"]:  # Solo jugadores que no hicieron fold
                if player["uuid"] == self.uuid:
                    # Guardamos las cartas de este jugador
                    self.game_state["final_hands"][player["name"]] = {
                        "cards": self.show_dowm_hole_cards,
                        "strength": None  # Se llenará después
                    }

        # Guardamos la fuerza de la mano (si está en hand_info)
        for info in hand_info:
            if info["uuid"] == self.uuid and info["uuid"] in [p["uuid"] for p in round_state["seats"]]:
                self.game_state["final_hands"][self.name]["strength"] = info["hand"]["hand"]["strength"]

        # Guardamos a los ganadores
        self.game_state["winners"] = winners


class HumanPlayer(BasePokerPlayer):
    def __init__(self, user_id,username):
        self.user_id = user_id
        self.name = username
        self.current_action = None
        self.waiting_for_action = False
        self.game_state = {}
        self.show_dowm_hole_cards =[]

    def declare_action(self, valid_actions, hole_card, round_state):
        self.game_state["valid_actions"] = valid_actions
        self.game_state["hole_card"] = hole_card
        self.game_state["round_state"] = round_state
        self.waiting_for_action = True
        self.show_dowm_hole_cards = hole_card

        while self.current_action is None:
            pass  # Espera la acción del usuario

        action = self.current_action
        self.current_action = None
        self.waiting_for_action = False
        print(action)
        return action

    def set_action(self, action, amount=0):
        self.current_action = (action, amount)

    def is_waiting_for_action(self):
        return self.waiting_for_action

    def receive_game_start_message(self, game_info):
        self.game_state["game_info"] = game_info

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.game_state["hole_card"] = hole_card
        self.game_state["seats"] = seats

    def receive_street_start_message(self, street, round_state):
        self.game_state["community_cards"] = round_state["community_card"]

    def receive_game_update_message(self, action, round_state):
        self.game_state["last_action"] = action

    def receive_round_result_message(self, winners, hand_info, round_state):
        """
        Guarda las cartas de todos los jugadores activos al finalizar la partida.
        
        """
        if "final_hands" not in self.game_state:
            self.game_state["final_hands"] = {}  # Inicializa solo una vez

        # Recorremos los jugadores que llegaron al showdown
        for player in round_state["seats"]:
            if player["state"] in ["participating", "allin"]:  # Solo jugadores que no hicieron fold
                if player["uuid"] == self.uuid:
                    # Guardamos las cartas de este jugador
                    self.game_state["final_hands"][player["name"]] = {
                        "cards": self.show_dowm_hole_cards,
                        "strength": None  # Se llenará después
                    }

        # Guardamos la fuerza de la mano (si está en hand_info)
        for info in hand_info:
            if info["uuid"] == self.uuid and info["uuid"] in [p["uuid"] for p in round_state["seats"]]:
                self.game_state["final_hands"][self.name]["strength"] = info["hand"]["hand"]["strength"]

        # Guardamos a los ganadores
        self.game_state["winners"] = winners

