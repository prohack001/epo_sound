import streamlit as st
import sqlite3
from database import get_user_by_credentials

def login():
    st.title("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        user = get_user_by_credentials(username, password)
        if user:
            st.session_state.user = {"id": user[0], "username": user[1]}
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

def logout():
    st.session_state.user = None
    st.rerun()
