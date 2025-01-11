import streamlit as st
from auth import login, logout
from chat import *
from database import init_db , get_user_sessions , create_new_session

# Initialisation de la base de données
init_db()

# Gestion de l'état utilisateur
if "user" not in st.session_state:
    st.session_state.user = None

# Barre latérale pour le login/logout et la liste des sessions
with st.sidebar:
    if st.session_state.user:
        st.markdown(f"### Connecté : {st.session_state.user['username']}")
        if st.button("Déconnexion"):
            logout()
    else:
        login()

    if st.session_state.user:
        st.markdown("## Mes sessions")
        user_id = st.session_state.user["id"]
        sessions = get_user_sessions(user_id)

        # Affichage des sessions dans la barre latérale
        for session_id, session_name in sessions:
            if st.button(session_name, key=f"session_{session_id}"):
                st.session_state.current_session = session_id
                st.rerun()
        # Ajouter une nouvelle session
        new_session_name = st.text_input("Nouvelle session")
        if st.button("Créer"):
            if new_session_name:
                create_new_session(user_id, new_session_name)
                st.success("Session créée avec succès !")
                st.rerun()
# Zone principale
if st.session_state.user:
    # render_chat_interface()
    render_header()
    render_chat_interface()
else:
    st.title("Bienvenue sur EPO_SOUND")
    st.write("Veuillez vous connecter pour utiliser l'application.")
