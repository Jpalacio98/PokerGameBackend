# Poker Game Backend

Este es el backend de un juego de poker desarrollado con Flask y PyPokerEngine. Proporciona autenticación de usuario, gestión de mesas y bots para jugar Texas Hold'em.

## 🚀 Instalación y Configuración

### **1. Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/PokerGameBackend.git
cd PokerGameBackend
```

### **2. Crear y activar un entorno virtual**

#### **Windows (PowerShell):**

```powershell
python -m venv env
venv\Scripts\activate
```

#### **Mac/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### **3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

### **4. Configurar la base de datos y migraciones**

Ejecuta los siguientes comandos en la terminal para configurar la base de datos:

```powershell
$env:FLASK_APP="run.py"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

En Mac/Linux, usa:

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### **5. Ejecutar el servidor**

Para iniciar la aplicación, ejecuta:

```bash
python run.py
```

El servidor se ejecutará en `http://127.0.0.1:5000/`.

## 📌 Endpoints Principales

### **Autenticación**

- **Registro:** `POST /register`

  ```json
  { "username": "testuser", "password": "123456" }
  ```

- **Login:** `POST /login`

  ```json
  { "username": "testuser", "password": "123456" }
  ```

### **Juego**

- **Crear mesa:** `POST /create_table`

  ```json
  { "level": 3, "big_blind": 10, "num_players": 6 }
  ```

- **Iniciar partida:** `POST /start_game`

  ```json
  { "level": 3 }
  ```

## 🛠 Tecnologías Usadas

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- PyPokerEngine

## 📜 Licencia

Este proyecto está bajo la licencia MIT.
