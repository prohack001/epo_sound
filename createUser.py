import sqlite3

# Chemin vers la base de données
DB_PATH = "chat_sessions.db"

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"Utilisateur '{username}' ajouté avec succès.")
    except sqlite3.IntegrityError:
        print(f"Le nom d'utilisateur '{username}' existe déjà.")
    finally:
        conn.close()

# Remplacer ces valeurs par les informations du premier utilisateur
create_user("epoadmin", "epo#123")
