import time
import streamlit as st
import sqlite3
from database import get_user_by_credentials ,set_token

import requests
# URL de l'API
API_URL = "https://audio-u7r5.onrender.com"
# API_URL = "https://epo-sound-api.onrender.com"

# Fonction pour appeler l'API de création d'utilisateur
def register_user(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{API_URL}/api/auth/register", json=data,headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Interface Streamlit
def signup_page():
    st.title("S'inscrire")
    st.write("Créez un compte pour accéder à la plateforme.")

    # Champs du formulaire
    firstname = st.text_input("Prénom", placeholder="Entrez votre prénom")
    lastname = st.text_input("Nom", placeholder="Entrez votre nom")
    email = st.text_input("Email", placeholder="Entrez votre email")
    password = st.text_input("Mot de passe", placeholder="Entrez votre mot de passe", type="password")

    # Termes et conditions
    agree_to_terms = st.checkbox("J'accepte les Termes et Conditions")

    # Afficher les messages d'erreur ou de succès
    if "error_message" not in st.session_state:
        st.session_state.error_message = None
    if "success_message" not in st.session_state:
        st.session_state.success_message = None

    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    if st.session_state.success_message:
        st.success(st.session_state.success_message)

    # Bouton d'envoi
    if st.button("Créer un compte"):
        if not agree_to_terms:
            st.warning("Vous devez accepter les Termes et Conditions pour continuer.")
        else:
            user_data = {
                "firstname": firstname.strip(),
                "lastname": lastname.strip(),
                "email": email.strip(),
                "password": password.strip(),
            }
            # Appel à l'API
            with st.spinner("Enregistrement en cours..."):
                response = register_user(user_data)

            # Gestion des réponses
            if "error" in response:
                st.session_state.error_message = response["error"]
                st.session_state.success_message = None
            elif response.get("message"):
                st.session_state.success_message = response["message"]
                st.session_state.error_message = None
                st.session_state["auth_page"] = "signin"
                # Redirection simulée après succès
                st.rerun()
                
    



def login_user(email, password):
    """Simule une authentification utilisateur."""
    if email == "test@example.com" and password == "password123":
        return {"success": True, "message": "Connexion réussie"}
    else:
        raise ValueError("Email ou mot de passe incorrect.")

# Interface Streamlit
def sign_in():
    st.title("Connexion")

    # Champs de saisie pour email et mot de passe
    email = st.text_input("Email", placeholder="Entrez votre email", key="email")
    password = st.text_input("Mot de passe", placeholder="Entrez votre mot de passe", type="password", key="password")
    remember_me = st.checkbox("Se souvenir de moi")

    # Bouton de connexion
    login_button = st.button("Se connecter")

    # Gestion des erreurs
    if login_button:
        with st.spinner("Connexion en cours..."):
            try:
                print(f"{email.strip()}")
                response = login(email.strip(), password.strip())
                if response['success']:
                    st.success("connexion réussie")
                    st.balloons()
                    st.experimental_set_query_params(page="dashboard")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                print(e)
                st.error("Une erreur est survenue. Veuillez réessayer plus tard.")

    # Lien vers la page d'inscription ou de récupération de mot de passe
    

def login(email,password):
        try:
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            payload = {
                "grant_type": "password",  
                "username": email,
                "password": password,
            }
            response = requests.post(f"{API_URL}/api/auth/token", data=payload, headers=headers)
            
            if response.status_code == 200:
                st.success("Connexion réussie!")
                print(response.json().get('user'))
                token = response.json().get('access_token')
                st.write(f"Token d'accès : {token}")
                set_token(token)
                st.session_state["user"] = response.json().get('user')
                st.rerun()
            else:
                print("response")
                raise ValueError(f"Erreur {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print("erreeuuuur")
            return {"error": str(e)}

def logout():
    st.session_state.user = None
    st.rerun()
