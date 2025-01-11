import streamlit as st
from database import get_session_messages, add_message
import json

# Fonction pour générer un token
def generate_token():
    st.session_state.token = "12345-ABCDE"  # Exemple de token
    st.success(f"Token généré : {st.session_state.token}")

# Interface principale du chat
def render_chat_interface():
    if "current_session" not in st.session_state:
        st.write("Veuillez sélectionner ou créer une session de chat.")
        return

    session_id = st.session_state.current_session
    messages = get_session_messages(session_id)

    st.markdown("""
    <style>
        .user-message {
            background-color: #e0f7fa;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            text-align: right;
        }
        .bot-message {
            background-color: #ffecb3;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            text-align: left;
        }
        .input-area {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #ffffff;
            padding: 10px;
            box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    # Affichage des messages
    for sender, message in messages:
        if sender == "user":
            st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)

    # Zone de saisie flottante
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    user_input = st.text_input("Message", placeholder="Tapez votre message ici...", key="user_input")
    if st.button("Envoyer"):
        if user_input:
            add_message(session_id, "user", user_input)
            # Simuler une réponse du modèle
            add_message(session_id, "bot", f"Réponse automatique à : {user_input}")
            st.rerun()
        else:
            st.warning("Veuillez entrer un message avant d'envoyer.")
    st.markdown('</div>', unsafe_allow_html=True)

# Header avec le choix du modèle, export, et profil
def render_header():
    with st.container():

        header_col1, header_col2, header_col3 = st.columns([2, 1, 1])

        with header_col1:
            selected_model = st.selectbox(
                "Choisir un modèle", 
                ["Classification de Bruit", "Prédiction de Qualité Vocale"], 
                key="selected_model"
            )
        
        # Export des discussions
        with header_col2:
            if st.button("Exporter les Discussions"):
                session_id = st.session_state.get("current_session", None)
                if session_id:
                    messages = get_session_messages(session_id)
                    if messages:
                        history_json = json.dumps(
                            [{"sender": msg[0], "text": msg[1]} for msg in messages],
                            indent=2,
                            ensure_ascii=False
                        )
                        st.download_button(
                            label="Télécharger l'Historique",
                            data=history_json,
                            file_name=f"epo_sound_{session_id}_history.json",
                            mime="application/json",
                        )
                    else:
                        st.warning("Aucune discussion à exporter.")
                else:
                    st.warning("Aucune session active.")

        # Profil utilisateur
        with header_col3:
            st.image(
                "https://via.placeholder.com/50", 
                caption="Profil", 
                width=50
            )  
            st.write("**Utilisateur**")




