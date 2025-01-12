import streamlit as st
from auth import login, logout,signup_page,sign_in
from chat import *
from database import init_db , get_user_sessions , create_new_session


# Initialisation de la base de données
init_db()

# Gestion de l'état utilisateur
if "user" not in st.session_state:
    st.session_state.user = None

if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "signin" 

if "traitement" not in st.session_state:
        st.session_state["traitement"] = None
        
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = None


# Barre latérale pour le login/logout et la liste des sessions
with st.sidebar:
    if st.session_state.user:
        st.markdown(f"### Connecté : {st.session_state.user['firstname']}")
        if st.button("Déconnexion"):
            logout()
    else:
        if st.session_state["auth_page"] == "signin":
            sign_in()
            if st.button("Créer un compte"):
                st.session_state["auth_page"] = "signup"
                st.rerun()
            # if st.markdown("Pas encore de compte ? [Créer un compte](#)", unsafe_allow_html=True):
            #     st.session_state["auth_page"] = "signup"
                # st.rerun()  
        elif st.session_state["auth_page"] == "signup":
            signup_page()
            if st.button("Se connecter"):
                st.session_state["auth_page"] = "signin"
                st.rerun()

    if st.session_state.user:
        st.markdown("## Mes sessions")
        user_id = st.session_state.user["uid"]
        sessions = get_user_sessions(user_id)

        # Affichage des sessions dans la barre latérale
        for session in sessions:
            session_id = session['id']
            session_name = session['session_name']
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
