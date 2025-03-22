# from pypokerengine.api.game import setup_config, start_poker
# from .bots import HonestPlayer, HumanPlayer
# import uuid

# # Diccionario global para almacenar jugadores humanos y su estado de juego
# human_players = {}

# def start_game(user_id, username, level=1):
#     """
#     Inicializa una partida con el usuario y bots de nivel específico.
#     """
#     config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)

#     # ✅ Registrar al usuario como jugador humano
#     human_player = HumanPlayer(user_id,username)
#     human_players[user_id] = human_player
#     config.register_player(username, human_player)

#     # ✅ Añadir bots al juego y almacenar sus UUIDs
#     bot_players = {}  # Diccionario para almacenar bots con su UUID
#     num_bots = min(level + 1, 5)  # Máximo 5 bots

#     for i in range(num_bots):
#         config.register_player(f"bot_{i+1}", HonestPlayer(f"bot_{i+1}"))
   

#     # ✅ Iniciar el juego en un hilo separado
#     import threading
#     game_thread = threading.Thread(target=start_poker, args=(config, 1))
#     game_thread.start()

#     return {
#         "msg": "Partida iniciada",
#         "user_id": user_id,
#         "game_info": human_player.game_state.get("game_info", {}),
#         "hole_card": human_player.game_state.get("hole_card", []),
#         "community_cards": human_player.game_state.get("community_cards", []),
#         "valid_actions": human_player.game_state.get("valid_actions", []),
#         "last_action": human_player.game_state.get("last_action", {}),
#         "round_results": human_player.game_state.get("round_results", {}),
#         "final_hands": human_player.game_state.get("final_hands", {}),  # Cartas de los jugadores en showdown
#         "winners": human_player.game_state.get("winners", {}),  # Ganadores de la partida
#         "bot_players": bot_players  # Devolvemos los bots con sus UUIDs
#     }



from pypokerengine.api.game import setup_config, start_poker
from .bots import HonestPlayer, HumanPlayer
import threading

# Diccionario global para almacenar jugadores humanos y su estado de juego
human_players = {}
bot_players = {}  # Diccionario para almacenar bots

def start_game(user_id, username, level=1):
    """
    Inicializa una partida con el usuario y bots de nivel específico.
    """
    config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)

    # ✅ Registrar al usuario como jugador humano
    human_player = HumanPlayer(user_id, username)
    human_players[user_id] = human_player
    config.register_player(username, human_player)

    # ✅ Añadir bots al juego y almacenarlos en un diccionario global
    num_bots = min(level + 1, 5)  # Máximo 5 bots
    for i in range(num_bots):
        bot_name = f"bot_{i+1}"
        bot_player = HonestPlayer(bot_name)
        bot_players[bot_name] = bot_player
        config.register_player(bot_name, bot_player)

    # ✅ Iniciar el juego en un hilo separado
    game_thread = threading.Thread(target=start_poker, args=(config, 1))
    game_thread.start()

    # ✅ Devolver la información del juego
    return {
        "msg": "Partida iniciada",
        "user_id": user_id,
        "game_info": human_player.game_state.get("game_info", {}),
        "hole_card": human_player.game_state.get("hole_card", []),
        "community_cards": human_player.game_state.get("community_cards", []),
        "valid_actions": human_player.game_state.get("valid_actions", []),
        "last_action": human_player.game_state.get("last_action", {}),
        "round_results": human_player.game_state.get("round_results", {}),
        "bot_players": list(bot_players.keys())  # Enviar solo nombres de los bots
    }


def get_final_hands():
    """
    Devuelve las cartas finales de todos los jugadores al finalizar la partida.
    """
    final_hands = {}

    # ✅ Agregar cartas del jugador humano
    for user_id, player in human_players.items():
        if "final_hands" in player.game_state:
            final_hands[player.name] = player.game_state["final_hands"]

    # ✅ Agregar cartas de los bots
    for bot_name, bot in bot_players.items():
        if "final_hands" in bot.game_state:
            final_hands[bot.name] = bot.game_state["final_hands"]

    return final_hands
