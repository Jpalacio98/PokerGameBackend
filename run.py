from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)  # Habilita migraciones de base de datos

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
