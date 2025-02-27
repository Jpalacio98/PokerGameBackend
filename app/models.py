from . import db
import uuid

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=1000.0)  # Saldo inicial del jugador

class GameSession(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    initial_balance = db.Column(db.Float, nullable=False)
    final_balance = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # "win" o "lose"
    amount_won_or_lost = db.Column(db.Float, nullable=False)
