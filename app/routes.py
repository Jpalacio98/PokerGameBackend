from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import GameSession, User, db
from .poker import get_final_hands, start_game, human_players

bp = Blueprint('routes', __name__)

@bp.route('/create_table', methods=['POST'])
@jwt_required()
def create_table():
    data = request.get_json()
    level = data.get('level')
    big_blind = data.get('big_blind')
    num_players = data.get('num_players')

    if not (1 <= level <= 10):
        return jsonify({"msg": "Invalid level"}), 400

    return jsonify({"msg": "Table created", "level": level, "big_blind": big_blind, "num_players": num_players})

bp = Blueprint('routes', __name__)

@bp.route('/start_game', methods=['POST'])
@jwt_required()
def start_new_game():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    level = request.json.get('level', 1)
    game_data = start_game(user_id, user.username, level)
    
    return jsonify(game_data)

@bp.route('/player_action', methods=['POST'])
@jwt_required()
def player_action():
    """
    Recibe la acción del jugador humano desde la API.
    """
    user_id = get_jwt_identity()
    
    if user_id not in human_players:
        return jsonify({"msg": "No hay partida activa para este usuario"}), 400

    action = request.json.get('action')
    amount = request.json.get('amount', 0)

    if action not in ['fold', 'call', 'raise']:
        return jsonify({"msg": "Acción inválida"}), 400

    human_players[user_id].set_action(action, amount)
    
    return jsonify({"msg": f"Acción {action} enviada con éxito"})

@bp.route('/game_state', methods=['GET'])
@jwt_required()
def get_game_state():
    user_id = get_jwt_identity()

    if user_id not in human_players:
        return jsonify({"msg": "No hay partida activa para este usuario"}), 400

    player = human_players[user_id]

    return jsonify({
        #"game_info": player.game_state.get("game_info", {}),
        "hole_card": player.game_state.get("hole_card", []),
        "community_cards": player.game_state.get("community_cards", []),
        "valid_actions": player.game_state.get("valid_actions", []),
        "last_action": player.game_state.get("last_action", {}),
        "round_results": player.game_state.get("round_results", {}),
        # 🔥 Ahora muestra las cartas de todos los jugadores
        "winners": player.game_state.get("winners", {}),
    })


@bp.route('/showdown', methods=['GET'])
@jwt_required()
def get_showdown_hands():
    """
    Devuelve las cartas de los jugadores activos cuando llega el showdown.
    """
    user_id = get_jwt_identity()
    
    if user_id not in human_players:
        return jsonify({"msg": "No hay partida activa para este usuario"}), 400

    player = human_players[user_id]

    return jsonify({
        "community_cards": player.game_state.get("community_cards", []),
        "final_hands": get_final_hands(),
        #"final_hands": player.game_state.get("final_hands", {}),  # Cartas de los jugadores activos en el showdown
        "winners": player.game_state.get("winners", {})  # Ganador(es) de la partida
    })