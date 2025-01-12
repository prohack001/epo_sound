import requests
import streamlit as st
# URL de base de l'API
API_BASE_URL = "https://audio-u7r5.onrender.com/api"  # Remplacez par l'URL de votre API

def set_token(access_token):
    global token
    token = access_token

def get_headers():
    return {"Authorization": f"Bearer {token}"} if token else {}

def init_db():
    """Initialisation de la base de données - inutile ici car géré côté serveur."""
    pass

def get_user_by_credentials(username, password):
    """Appelle l'API pour vérifier les identifiants de l'utilisateur."""
    response = requests.post(f"{API_BASE_URL}/auth/login", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()  # Retourne l'objet utilisateur sous forme de dict
    return None

def get_user_sessions(user_id):
    """Appelle l'API pour récupérer les sessions de l'utilisateur."""

    response = requests.get(f"{API_BASE_URL}/session",headers=get_headers())
    # print(response.json(     ))
    if response.status_code == 200:
        return response.json()  
    return []

def get_session_messages(session_id):
    """Appelle l'API pour récupérer les messages d'une session."""
    print(session_id)
    response = requests.get(f"{API_BASE_URL}/message/{session_id}",headers=get_headers())
    print(response.json())
    if response.status_code == 200:
        return response.json()  # Retourne une liste de messages
    
    return []

def add_message(session_id, sender, message):
    """Appelle l'API pour envoyer un message dans une session."""
    response = requests.post(f"{API_BASE_URL}/message",headers=get_headers(), json={"session_id": session_id,"sender":sender ,"message": message})
    print(response.json())
    return response.status_code == 201  # Retourne True si le message a été ajouté avec succès

def create_new_session(user_id, session_name):
    """Appelle l'API pour créer une nouvelle session."""
    response = requests.post(
    f"{API_BASE_URL}/session",
    params={"user_id": user_id},
    headers=get_headers(),
    json={"session_name": session_name}
    )

    return response.status_code == 201  # Retourne True si la session a été créée avec succès
