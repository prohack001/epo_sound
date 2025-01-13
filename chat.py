import streamlit as st
from database import get_session_messages, add_message
import json
from streamlit_modal import Modal

models = {
    "classification": {
        "decision_tree": ["Vn", "ZCR", "SF", "CGS", "CS"],
        "bagging": ["Vn", "ZCR", "SF", "CGS"],
        "adaBoost": ["Vn", "ZCR", "SF", "CGS", "CS"],
        "random_forest": ["Vn", "ZCR", "SF", "CGS", "CS"]
    },
    "regression": {
        "decision_tree": ["Vn", "ZCR", "CGS", "SNR"],
        "bagging": ["Vn", "ZCR", "CGS", "SNR"],
        "random_forest": ["Vn", "ZCR", "CGS", "SNR"],
        "svm": ["ZCR", "Vn", "SNR", "SF"],
        "ridge": ["ZCR", "Vn", "SNR", "CGS"]
    }
}

tips = {
    "classification": "La meilleure classification, c’est **Random Forest Classifier** avec un score de 0.94.",
    "regression": "La meilleure régression, c’est **Bagging Regressor** avec un RMSE de 0.38."
}


modal = Modal(key="choix_modal", title="Choisir un mode", max_width=600)

# Interface principale du chat
def render_chat_interface():
    inputs = {}
    
    if st.session_state["selected_model"]:
        traitement = st.session_state["traitement"]
        selected_model = st.session_state["selected_model"]
        st.success(f"Mode : **{traitement}**, Modèle : **{selected_model}** sélectionné.")
    # Affichage des paramètres dynamiques après sélection
    

    if "current_session" not in st.session_state:
        st.write("Veuillez sélectionner ou créer une session de chat.")
        modal.open()
        return

    if modal.is_open():
        with modal.container():
            st.subheader("Choisissez le type de traitement")
            traitement = st.radio("Type de traitement", ["classification", "regression"], key="traitement_modal")
            if traitement in tips:
                st.info(tips[traitement])

            # Afficher les modèles associés au type de traitement sélectionné
            model_options = list(models[traitement].keys())
            selected_model = st.selectbox("Modèle", model_options, key="model_modal")

            # Bouton pour confirmer le choix
            if st.button("Confirmer"):
                st.session_state["traitement"] = traitement
                st.session_state["selected_model"] = selected_model
                modal.close()

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
    for message_data in messages:
        sender = message_data['sender']
        if sender == "bot":
            message = message_data['prediction']
            if message_data['model_type']=="classification":
                print("rentre")
                message = int(message_data['prediction'])
                if message == 0:
                    message="environnement"
                elif message== 2:
                    message="souffle"
                else:
                    message="grésillement"
            else:
                if 0 <= message <= 1:
                    message= "qualité médiocre"
                elif 1 < message <= 2:
                    message ="qualité faible"
                elif 2 < message <= 3:
                    message ="qualité moyenne"
                elif 3 < message <= 4:
                    message ="qualité bonne"
                elif 4 < message <= 5:
                    message ="qualité excellente"
                
        else:
            message = message_data['message']
        
        if sender == "bot":
            st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)

    if st.session_state["selected_model"]:
        

        
        st.write("Veuillez remplir les champs suivants :")
    

        # params = models[traitement][selected_model]
        # default_data = {param: [0.0] for param in params}  # Valeurs par défaut
        # table_data = st.data_editor(default_data, key="data_editor", num_rows=1)  # Tableau avec une seule ligne

        # incomplete_fields = any(value == 0.0 for value in table_data.values())


        for param in models[traitement][selected_model]:
            inputs[param] = st.text_input(f"Paramètre {param}", key=f"{param}_input")
    # Zone de saisie flottante
    # st.markdown('<div class="input-area">', unsafe_allow_html=True)
    # user_input = st.text_input("Message", placeholder="Tapez votre message ici...", key="user_input")
    if st.button("Envoyer"):
        try:
            # Convertir toutes les entrées en float et construire le JSON
            
            #json_data={}
            json_data = {
                "session_id": st.session_state.current_session, 
                "message": { key: float(value) for key, value in inputs.items() },
                "model_type": traitement,
                "algorithm": selected_model
            }
            # json_data["session_id"] = int(st.session_state.current_session)
            # json_data["message"] = {key: float(value) for key, value in inputs.items()}
            # json_data["model_type"] = traitement
            # json_data["algorithm"] = selected_model

            # Conversion en chaîne JSON formatée
            json_formatted = json.dumps(json_data, indent=None, separators=(', ', ': '))
            # json_data["session_id"]=st.session_state.current_session
            # json_data["message"]={key: float(value) for key, value in inputs.items()}
            # json_data["model_type"] = traitement
            # json_data["algorithm"] = selected_model
            print("json_sata: ",json_data)
            #message_json = json.dumps(json_data, indent=1)
            print("message_json: ",json_formatted)
            add_message(json_data)
            st.json(json_data) 
            st.rerun()
        except ValueError as e:
            st.error(f"Erreur : Veuillez saisir uniquement des nombres pour tous les paramètres.")

        # if user_input:
        #     add_message(session_id, "user", user_input)
        #     # Simuler une réponse du modèle
        #     # add_message(session_id, "bot", f"Réponse automatique à : {user_input}")
        #     st.rerun()
        # else:
        #     st.warning("Veuillez entrer un message avant d'envoyer.")
    st.markdown('</div>', unsafe_allow_html=True)

# Header avec le choix du modèle, export, et profil
def render_header():
    with st.container():

        header_col1, header_col2, header_col3 = st.columns([2, 1, 1])

        with header_col1:
            # selected_model = st.selectbox(
            #     "Choisir un modèle", 
            #     ["Classification de Bruit", "Prédiction de Qualité Vocale"], 
            #     key="selected_model"
            # )
            
            if st.button("Choisir mode"):
                modal.open()
                st.rerun()
        
        
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
                "https://cdn.pixabay.com/photo/2024/09/05/20/13/ai-generated-9026025_1280.jpg", 
                caption=st.session_state.user["firstname"], 
                width=50
            ) 




